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
        "note": "Clean-environment reproduction of pinned synthetic references. Not authenticity, certification, or operational readiness.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.workspace), sort_keys=True))


if __name__ == "__main__":
    main()
