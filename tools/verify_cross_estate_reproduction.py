#!/usr/bin/env python3
"""Verify a clean exact-SHA cross-estate checkout. Standard library only.

The verifier hashes pinned files and reads commit metadata already present in
the workspace. It does not fetch, grant authority, infer authenticity, or
infer operational readiness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "contracts" / "cross-estate-reproduction.lock.json"
GRAPH = ROOT / "contracts" / "federated-evidence-graph.example.json"
PORTFOLIO = ROOT / "portfolio.json"
COMMIT = re.compile(r"^[a-f0-9]{40}$")
DIGEST = re.compile(r"^sha256:[a-f0-9]{64}$")
ORG_REPOSITORY = ".github"
BINDING_TYPES = {"SAME_SUBJECT", "COMPONENT_OF", "SUPPORTING_EVIDENCE_FOR"}
BINDING_KEYS = {
    "binding_id",
    "reference_id",
    "binding_type",
    "thread_subject_id",
    "thread_configuration_digest",
    "native_subject_id",
    "native_configuration_digest",
    "limitations",
    "authority_effect",
}


class ReproductionError(Exception):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReproductionError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReproductionError(f"{path.name}: {exc}") from exc


def _head(checkout: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ReproductionError(f"commit metadata unavailable for {checkout.name}") from exc



def _validate_federated_bindings(thread: dict[str, Any], payloads: dict[str, dict]) -> int:
    bindings = thread.get("subject_bindings")
    _require(isinstance(bindings, list), "subject_bindings required")
    references = thread.get("references")
    _require(isinstance(references, list), "golden thread references required")
    by_id = {ref["reference_id"]: ref for ref in references}
    by_binding: dict[str, dict] = {}
    seen_ids: set[str] = set()
    for binding in bindings:
        _require(isinstance(binding, dict) and set(binding) == BINDING_KEYS, "unsupported binding fields")
        _require(isinstance(binding.get("binding_id"), str) and binding["binding_id"].strip(), "binding_id required")
        _require(binding["binding_id"] not in seen_ids, "duplicate binding_id")
        seen_ids.add(binding["binding_id"])
        ref_id = binding.get("reference_id")
        _require(ref_id in by_id, "binding points to a missing reference")
        _require(ref_id not in by_binding, "duplicate binding")
        ref = by_id[ref_id]
        _require("subject_id" in ref or "configuration_digest" in ref, "binding requires a subject-bearing reference")
        _require(binding.get("binding_type") != "AUTHORIZES", "binding cannot grant authority")
        _require(binding.get("binding_type") in BINDING_TYPES, "unsupported binding type")
        _require(binding.get("authority_effect") == "NONE", "binding authority transfer")
        _require(binding.get("thread_subject_id") == thread.get("subject_id"), "thread subject mismatch")
        _require(
            binding.get("thread_configuration_digest") == thread.get("configuration_digest"),
            "thread configuration mismatch",
        )
        _require(binding.get("native_subject_id") == ref.get("subject_id"), "native subject mismatch")
        _require(binding.get("native_configuration_digest") == ref.get("configuration_digest"), "native configuration mismatch")
        if binding["binding_type"] == "SAME_SUBJECT":
            _require(
                binding["native_subject_id"] == binding["thread_subject_id"]
                and binding["native_configuration_digest"] == binding["thread_configuration_digest"],
                "false SAME_SUBJECT",
            )
        else:
            limitations = binding.get("limitations")
            _require(isinstance(limitations, list) and limitations, "missing binding limitation")
            _require(all(isinstance(item, str) and item.strip() for item in limitations), "missing binding limitation")
            text = " ".join(limitations).lower()
            _require("synthetic" in text and "not external proof" in text, "binding is not an explicit synthetic declaration")
        payload = payloads.get(ref_id)
        if isinstance(payload, dict):
            if "subject_id" in payload:
                _require(payload["subject_id"] == binding["native_subject_id"], "payload subject mismatch")
            if "configuration_digest" in payload:
                _require(payload["configuration_digest"] == binding["native_configuration_digest"], "payload configuration mismatch")
        by_binding[ref_id] = binding
    for ref_id, ref in by_id.items():
        if "subject_id" in ref or "configuration_digest" in ref:
            _require(ref_id in by_binding, "unbound native reference")
    scenarios = {item["id"]: item for item in thread.get("scenarios", []) if isinstance(item, dict)}
    for scenario_id in ("dependency-failure", "succession-failure"):
        native_ref = scenarios.get(scenario_id, {}).get("native_reference")
        _require(native_ref in by_binding, "failure scenario points to an unbound native reference")
        _require(by_id[native_ref].get("expected_outcome") == "FAILED", "native failure fixture is not FAILED")
    return len(by_binding)


def _binding_payloads(thread: dict[str, Any], workspace: Path) -> dict[str, dict]:
    payloads: dict[str, dict] = {}
    for ref in thread.get("references", []):
        path = workspace / ref["source_repository"] / ref["artifact_path"]
        if path.is_file() and path.suffix == ".json":
            payload = _load(path)
            if isinstance(payload, dict):
                payloads[ref["reference_id"]] = payload
    return payloads


def prove_binding_negatives(thread: dict[str, Any], workspace: Path, artifacts: list[dict]) -> None:
    payloads = _binding_payloads(thread, workspace)

    def reject(label: str, mutated: dict, mutated_payloads: dict | None = None) -> None:
        try:
            _validate_federated_bindings(mutated, mutated_payloads or payloads)
        except ReproductionError:
            return
        raise ReproductionError(f"negative binding case was accepted: {label}")

    unbound = json.loads(json.dumps(thread))
    unbound["subject_bindings"] = [item for item in unbound["subject_bindings"] if item["reference_id"] != "evidence-object"]
    reject("unbound native reference", unbound)

    duplicate = json.loads(json.dumps(thread))
    duplicate["subject_bindings"].append(dict(duplicate["subject_bindings"][0], binding_id="binding-duplicate"))
    reject("duplicate binding", duplicate)

    missing = json.loads(json.dumps(thread))
    missing["subject_bindings"][0]["reference_id"] = "missing-reference"
    reject("binding to missing reference", missing)

    thread_subject = json.loads(json.dumps(thread))
    thread_subject["subject_bindings"][0]["thread_subject_id"] = "other-mission"
    reject("thread subject mismatch", thread_subject)

    thread_config = json.loads(json.dumps(thread))
    thread_config["subject_bindings"][0]["thread_configuration_digest"] = "sha256:" + "11" * 32
    reject("thread configuration mismatch", thread_config)

    native_subject = json.loads(json.dumps(thread))
    native_subject["subject_bindings"][0]["native_subject_id"] = "other-subject"
    reject("native subject mismatch", native_subject)

    native_config = json.loads(json.dumps(thread))
    native_config["subject_bindings"][0]["native_configuration_digest"] = "sha256:" + "22" * 32
    reject("native configuration mismatch", native_config)

    false_same = json.loads(json.dumps(thread))
    false_same["subject_bindings"][0]["binding_type"] = "SAME_SUBJECT"
    reject("false SAME_SUBJECT", false_same)

    unsupported = json.loads(json.dumps(thread))
    unsupported["subject_bindings"][0]["binding_type"] = "AUTHORIZES"
    reject("unsupported binding type", unsupported)

    authority = json.loads(json.dumps(thread))
    authority["subject_bindings"][0]["authority_effect"] = "AUTHORIZE"
    reject("authority transfer", authority)

    missing_limitation = json.loads(json.dumps(thread))
    missing_limitation["subject_bindings"][0]["limitations"] = []
    reject("missing binding limitation", missing_limitation)

    golden = next(item for item in artifacts if item["path"].endswith("golden-thread.json"))
    golden_path = workspace / golden["repository"] / golden["path"]
    try:
        _require(_sha256(golden_path) == "0" * 64, "digest mismatch")
    except ReproductionError:
        pass
    else:
        raise ReproductionError("tampered artifact digest was accepted")
    try:
        _require(_head(workspace / golden["repository"]) == "0" * 40, "checkout commit mismatch")
    except ReproductionError:
        pass
    else:
        raise ReproductionError("wrong pinned commit was accepted")


def verify(workspace: Path) -> dict[str, Any]:
    lock = _load(LOCK)
    portfolio = _load(PORTFOLIO)
    graph = _load(GRAPH)
    _require(isinstance(lock, dict), "lock must be an object")
    _require(lock.get("reference_only") is True, "lock reference_only must be true")
    _require(lock.get("authority_effect") == "NONE", "lock authority_effect must be NONE")
    _require(portfolio.get("owner") == "GLOBAL-AI-GOVERNANCE", "unexpected source owner")
    owned = {item["repository"] for item in portfolio["repositories"]}
    owned.add(ORG_REPOSITORY)
    repositories = lock.get("repositories")
    artifacts = lock.get("artifacts")
    _require(isinstance(repositories, list) and repositories, "repositories required")
    _require(isinstance(artifacts, list) and artifacts, "artifacts required")
    pins: dict[str, str] = {}
    for item in repositories:
        name = item.get("repository")
        sha = item.get("commit_sha")
        _require(isinstance(name, str) and name in owned, f"unsupported source repository: {name}")
        _require(COMMIT.fullmatch(str(sha)), f"malformed commit for {name}")
        _require(name not in pins, f"duplicate repository pin: {name}")
        checkout = workspace / name
        _require(checkout.is_dir(), f"missing checkout: {name}")
        _require(_head(checkout) == sha, f"checkout commit mismatch: {name}")
        pins[name] = sha
    seen_paths: set[tuple[str, str]] = set()
    for artifact in artifacts:
        name = artifact.get("repository")
        sha = artifact.get("commit_sha")
        rel = artifact.get("path")
        _require(name in pins, f"artifact repository is not pinned: {name}")
        _require(sha == pins[name], f"artifact commit is not the pinned commit: {rel}")
        _require(isinstance(rel, str) and rel and ".." not in Path(rel).parts, f"artifact path rejected: {rel}")
        _require((name, rel) not in seen_paths, f"duplicate artifact: {name}:{rel}")
        seen_paths.add((name, rel))
        _require(COMMIT.fullmatch(str(sha)), "malformed artifact commit")
        _require(re.fullmatch(r"[a-f0-9]{64}", str(artifact.get("sha256", ""))), f"malformed lock digest: {rel}")
        _require(artifact.get("authority_effect") == "NONE", f"artifact authority_effect must be NONE: {rel}")
        _require(isinstance(artifact.get("artifact_type"), str) and artifact["artifact_type"].strip(), "artifact type required")
        path = workspace / name / rel
        _require(path.is_file(), f"missing artifact: {name}:{rel}")
        actual = _sha256(path)
        _require(actual == artifact["sha256"], f"digest mismatch: {name}:{rel}")
        if path.suffix == ".json":
            payload = _load(path)
            _require(isinstance(payload, dict), f"artifact must be a JSON object: {rel}")
            if "authority_effect" in payload:
                _require(payload["authority_effect"] == "NONE", f"artifact grants authority: {rel}")
            if "reference_only" in payload:
                _require(payload["reference_only"] is True, f"artifact is not reference-only: {rel}")
            if "expected_outcome" in artifact:
                _require(payload.get("outcome") == artifact["expected_outcome"], f"outcome mismatch: {rel}")
            if "expected_subject_id" in artifact and "subject_id" in payload:
                _require(payload["subject_id"] == artifact["expected_subject_id"], f"subject mismatch: {rel}")
            if "expected_configuration_digest" in artifact and "configuration_digest" in payload:
                _require(
                    payload["configuration_digest"] == artifact["expected_configuration_digest"],
                    f"configuration mismatch: {rel}",
                )
    thread_pin = next(
        item for item in artifacts if item["path"] == "automation/assurance/mission-assurance/challenge/golden-thread.json"
    )
    thread = _load(workspace / thread_pin["repository"] / thread_pin["path"])
    _require(thread.get("authority_effect") == "NONE", "golden thread authority_effect must be NONE")
    _require(thread.get("reference_only") is True, "golden thread must be reference-only")
    _require(thread.get("automatic_requalification") is False, "golden thread must not auto-requalify")
    _require(isinstance(thread.get("subject_id"), str) and thread["subject_id"].strip(), "golden thread subject required")
    _require(DIGEST.fullmatch(str(thread.get("configuration_digest", ""))), "golden thread configuration malformed")
    by_subject: dict[str, str] = {}
    references = thread.get("references")
    _require(isinstance(references, list) and references, "golden thread references required")
    for ref in references:
        name = ref.get("source_repository")
        rel = ref.get("artifact_path")
        _require(name in pins, f"golden-thread source is not owned: {name}")
        _require(ref.get("source_commit") == pins[name], f"golden-thread commit mismatch: {rel}")
        _require(ref.get("authority_effect") == "NONE", f"golden-thread reference grants authority: {rel}")
        _require(DIGEST.fullmatch(str(ref.get("artifact_digest", ""))), f"golden-thread digest malformed: {rel}")
        matched = [item for item in artifacts if item["repository"] == name and item["path"] == rel]
        _require(len(matched) == 1, f"golden-thread reference is not locked: {name}:{rel}")
        path = workspace / name / rel
        actual = _sha256(path)
        _require(ref["artifact_digest"] == "sha256:" + actual, f"golden-thread digest mismatch: {rel}")
        _require(matched[0]["artifact_type"] == ref.get("artifact_type"), f"golden-thread type mismatch: {rel}")
        payload = _load(path)
        if "subject_id" in ref and "subject_id" in payload:
            _require(ref["subject_id"] == payload["subject_id"], f"golden-thread subject mismatch: {rel}")
        if "configuration_digest" in ref and "configuration_digest" in payload:
            _require(ref["configuration_digest"] == payload["configuration_digest"], f"golden-thread configuration mismatch: {rel}")
        if "expected_outcome" in ref:
            _require(payload.get("outcome") == ref["expected_outcome"], f"golden-thread outcome mismatch: {rel}")
        subject = ref.get("subject_id")
        config = ref.get("configuration_digest")
        if isinstance(subject, str) and isinstance(config, str):
            prior = by_subject.get(subject)
            _require(prior in (None, config), f"subject/configuration inconsistency: {subject}")
            by_subject[subject] = config
    payloads = _binding_payloads(thread, workspace)
    bindings = _validate_federated_bindings(thread, payloads)
    prove_binding_negatives(thread, workspace, artifacts)
    for node in graph.get("nodes", []):
        name = node["source_repository"]
        _require(name in pins, f"graph source is not pinned: {name}")
        _require(node["source_commit"] == pins[name], f"graph commit mismatch: {node['node_id']}")
        _require(node["authority_effect"] == "NONE", f"graph node grants authority: {node['node_id']}")
        matched = [item for item in artifacts if item["repository"] == name and item["path"] == node["artifact_id"]]
        if not matched:
            continue
        _require(node["artifact_digest"] == "sha256:" + matched[0]["sha256"], f"graph digest mismatch: {node['node_id']}")
        _require(node["artifact_type"] == matched[0]["artifact_type"], f"graph type mismatch: {node['node_id']}")
        if "expected_subject_id" in matched[0]:
            _require(node["subject_id"] == matched[0]["expected_subject_id"], f"graph subject mismatch: {node['node_id']}")
        if "expected_configuration_digest" in matched[0]:
            _require(
                node["configuration_digest"] == matched[0]["expected_configuration_digest"],
                f"graph configuration mismatch: {node['node_id']}",
            )
    return {
        "valid": True,
        "reference_only": True,
        "authority_effect": "NONE",
        "repositories": len(pins),
        "artifacts": len(artifacts),
        "bindings": bindings,
        "artifact_reproduction": "VERIFIED",
        "federated_binding_consistency": "VERIFIED",
        "real_world_relationship_authenticity": "NOT_VERIFIED",
        "note": "Clean-environment reproduction of pinned synthetic references. Synthetic bindings are not external authenticity, certification, or operational readiness.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.workspace), sort_keys=True))


if __name__ == "__main__":
    main()
