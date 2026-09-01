# Release provenance migration receipt

This bounded historical receipt records how the August 2026 history sanitation affected five existing public release identities. It is not a release dashboard and does not request another rewrite, retag, or release.

| Release | Historical signed release-evidence commit | Current live tag commit | Shared Git tree |
|---|---|---|---|
| Global AI Governance Toolkit `v2.3.0` | `524b787f435d2efabdb83d7c1d356398a50c47ce` | `467717e0ceb48c52239694ca978707d20cfba67f` | `672280a34d38ce1f93238958408bde4eb42f68cc` |
| Agentic AI Governance `v0.1.0-alpha.2` | `937d09ec0cd52c2fe4164a97e86d542fd108aa15` | `d557afc9778cbedcb6e50c9e97a2173d304db68c` | `cc5dbd4da9d10b2c78fd693d2f530d57f19cd5fb` |
| Verified Vulnerability Governance `v0.1.3` | `b06700e5254c855cd1bb2cc85ec3595a63d9e1e1` | `07d74fdc5f98ed2959482715e8c5a38f98e7f5fd` | `afe4a83f734a4e3f2ce20e3d6c20d6f9c4bc1a06` |
| AI Cyber Resilience Framework `v0.1.1` | `84490f2b67b653eabf5394131fc8fd196f84c397` | `bf16ec00bc6e03767d5420bf52b984bbe33d9157` | `fa78c4b7635f504a2401c22c7d7fefaf3929fb0a` |
| Peace OS Crisis Room `v0.3.0-rc2` | `aa6d8f75ce755fd143a4aa457eadf91b54604bd5` | `8a40d94fcee14a6d6eb76782319bb90f0cec6202` | `d92212c36535b8e196805d24667a952bb148ccdf` |

For every row, direct Git object inspection established both conclusions:

- `CONTENT_PRESERVED`: the historical and current commits resolve to the same Git tree, so the release source content did not change in the mapping.
- `PROVENANCE_REANCHORED_BY_HISTORY_SANITATION`: the live tag now names a distinct post-sanitation commit identity.

Any original cryptographic signature remains evidence for its historical signed commit only. It did not transfer to, and this receipt does not claim it authenticates, the rewritten commit. Current release names and versions remain unchanged.
