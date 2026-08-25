# Story Generation Benchmark Dataset

Public, screenplay-text-free release of the data artifacts used by a feature-curve-guided screenplay rewriting research pipeline.

## Release snapshot

- **Version:** 1.0.1 (2026-08-25)
- **Film set:** `current_10_films_balanced_v1`
- **Films:** 10
- **Cleaned experimental scenes:** 938
- **Narrative feature axes:** 5
- **Feature annotations:** 938 × 5
- **TasksetV5:** 240 controlled rewriting tasks
- **Base intervals:** 48
- **Directed film pairs:** 24 (12 unordered pairs, evaluated bidirectionally)

## Important: screenplay text is not distributed

This repository **does not contain full screenplay text or any `script.json` screenplay files**. The experimental screenplay inputs were traced to a historical public revision of [`roytian1992/STAGE_v0`](https://github.com/roytian1992/STAGE_v0), specifically commit `ce4468eac15775a85e5cd3a2e7255d96ff1afb45`, where per-movie English `script.json` files were present at the time of access.

The historical source is recorded for provenance only. Public availability of a historical Git revision does not by itself grant redistribution or relicensing rights in the underlying screenplays. See [RIGHTS.md](RIGHTS.md).

## Provenance chain

```text
IMSDb source URLs recorded by STAGE
        ↓
historical STAGE_v0 English script.json snapshot
        ↓
local duplicate / source-artifact cleaning
        ↓
10-film cleaned experimental corpus (938 scenes)
        ↓
Feature Extraction V1.4 / Measurement Core V1.1
        ↓
938 per-scene × 5 narrative feature annotations
        ↓
TasksetV5
        ↓
240 controlled rewriting tasks
```

The exact STAGE movie IDs, immutable upstream commit/path/blob SHA-1, original source URLs, source scene counts, cleaned scene counts, and cleaned-input SHA-256 values are in [`metadata/source_provenance.csv`](metadata/source_provenance.csv).

## Source cleaning audit

The historical snapshot contains 1,101 scene records across the selected films; the cleaned experimental corpus contains 938. The 163-record reduction is exactly accounted for by three duplicated screenplay passes:

| Film | Historical records | Cleaned records | Removed |
|---|---:|---:|---:|
| Chasing Amy | 68 | 34 | 34 |
| Dog Day Afternoon | 138 | 69 | 69 |
| Apocalypse Now | 120 | 60 | 60 |
| **Total** | **326** | **163** | **163** |

For the remaining films, scene counts are unchanged. The White Ribbon required removal of non-screenplay IMSDb footer/page material appended to its final scene; Ghostbusters II and The Private Life of Sherlock Holmes differ from the historical bytes only by an EOF serialization newline; four other files were byte-identical in the audited historical snapshot.

A duplicate scan over the cleaned 938-scene corpus found zero duplicate groups under exact, whitespace-normalized, and more aggressive normalized-content comparisons. See [`metadata/source_alignment_audit.json`](metadata/source_alignment_audit.json).

## Repository layout

```text
.
├── data/
│   ├── corpus/                 # film IDs, counts, cleaned-input hashes
│   ├── features/               # 938 portable per-scene feature rows
│   ├── taskset_v5/             # 240 tasks + 48 base intervals + validation
├── instrument/                 # exact feature prompt/schema + sanitized protocol config
├── metadata/                   # provenance, definitions, manifests, preprocessing audit
├── preprocessing/              # deterministic reconstruction specification
├── scripts/                    # release validator + local reconstruction helper
├── checksums/SHA256SUMS
├── DATASET_CARD.md
├── RIGHTS.md
└── CITATION.cff
```

## Feature annotations

[`data/features/scene_features.jsonl`](data/features/scene_features.jsonl) has one row per cleaned scene. It intentionally omits screenplay titles and text. Fields:

- `film_id`
- `scene_id`
- `scene_index`
- `measurement_status`
- `pacing`
- `dialogue_density`
- `action_density`
- `character_interaction`
- `emotion_intensity`

All five feature values are continuous scores in `[0,1]`. The exact extraction prompt and JSON schema are in [`instrument/`](instrument/).

The canonical feature extraction completed **938/938 scenes with 0 measurement failures**.

## TasksetV5

[`data/taskset_v5/taskset.json`](data/taskset_v5/taskset.json) is the portable public form of the runtime TasksetV5 bundle. Absolute local paths were removed; task IDs, film IDs, scene IDs, interval assignment, feature axis, variants, difficulty metadata, pair policy, protocol hashes, and canonical structure hash were retained.

Key balances:

- 240 tasks
- 48 base intervals
- 24 directed pairs / 12 unordered pairs
- 48 tasks per feature axis
- 80 short / 80 medium / 80 long tasks
- canonical runtime structure SHA-256: `sha256:840aafe93408d41f3ef2e8fe791b0401ce52008060031a58aa46e4e28944bcdb`

## Reconstructing the cleaned input corpus

This repository does not download or distribute screenplay text. If you already possess a lawful local copy of the historical STAGE English `script.json` files from commit `ce4468eac15775a85e5cd3a2e7255d96ff1afb45`, run:

```bash
python3 scripts/reconstruct_cleaned_corpus.py \
  --stage-english-root /path/to/STAGE_v0/English \
  --output-root /tmp/storygen_cleaned_films
```

The script applies the audited deterministic cleaning rules and refuses success unless all ten output files match the experimental cleaned SHA-256 values. The rules are also machine-readable in [`preprocessing/reconstruction_spec.json`](preprocessing/reconstruction_spec.json).

## Validate this release

No third-party Python package is required:

```bash
python3 scripts/validate_release.py
```

Expected result: `PUBLIC RELEASE VALIDATION: PASS`.

## Historical STAGE revisions recorded for provenance

- Script-containing data-only snapshot used for file-level alignment: `ce4468eac15775a85e5cd3a2e7255d96ff1afb45`
- Later scene-reference repair commit: `9abbdffd280da0a625411b67c2eae8dfcdd846e4`
- Last verified pre-removal parent snapshot: `d902abfa51bf71ac10f53313a7add8b6ad5b1092`
- Release transition that stopped distributing the historical screenplay files: `809ea665783879da77f4f30bf7f5be771525f514`

These identifiers document lineage; this repository does not mirror those screenplay files.

## Citation

See [`CITATION.cff`](CITATION.cff). If a paper DOI or archival dataset DOI is assigned later, add it there and tag the corresponding immutable release.
