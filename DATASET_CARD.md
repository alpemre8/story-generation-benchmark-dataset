# Dataset Card

## Dataset summary

This release contains derived narrative feature measurements, a controlled rewriting taskset, reliability measurements, and provenance metadata for a 10-film screenplay research corpus. Full screenplay text is intentionally excluded.

## Dataset composition

| Component | Size |
|---|---:|
| Films | 10 |
| Cleaned scenes | 938 |
| Feature axes | 5 |
| Per-scene feature rows | 938 |
| Scalar feature values | 4,690 |
| TasksetV5 tasks | 240 |
| Base intervals | 48 |
| Directed pairs | 24 |
| Reliability scenes | 100 |
| Reliability repeats | 5 |
| Reliability measurements | 500 |
| Valid reliability measurements | 500 |

## Narrative features

The five measured dimensions are pacing, dialogue density, action density, character interaction, and emotion intensity. They are produced on a continuous `[0,1]` scale by the feature measurement instrument bundled under `instrument/`.

## Measurement configuration

- Model alias: `qwen2.5-7b-q4`
- Checkpoint format: GGUF
- Quantization: Q4_K_M
- Model SHA-256: `65b8fcd92af6b4fefa935c625d1ac27ea29dcb6ee14589c55a8f115ceaaa1423`
- llama.cpp commit: `1425386fd996511e1f3295e7366c38289a92a271`
- Temperature: 0.0
- Max tokens: 256
- Concurrency: 8
- Context per slot: 12,288
- Structured output: JSON Schema
- Measurement failures: 0 / 938

Local filesystem paths and localhost endpoint details from the runtime manifests were removed because they have no scientific value in the public release.

## Source provenance and preprocessing

The input scripts were traced to historical STAGE_v0 commit `ce4468eac15775a85e5cd3a2e7255d96ff1afb45`. The selected historical files contained 1,101 scene records; the experimental cleaned corpus contained 938. Duplicate-pass removal from Chasing Amy, Dog Day Afternoon, and Apocalypse Now accounts for all 163 removed records. A non-screenplay IMSDb footer was also removed from The White Ribbon without changing its scene count.

The exact per-film lineage and hashes are recorded in `metadata/source_provenance.csv` and `metadata/preprocessing_manifest.csv`.

## Intended use

The public data are intended for reproducibility, audit, benchmarking, and analysis of the associated feature-curve-guided rewriting experiments. The taskset identifies scene intervals and feature targets without redistributing screenplay text.

## Limitations

1. Feature annotations are model-based measurements, not human ground-truth labels.
2. The 10-film set is a controlled experimental corpus, not a representative sample of all screenplays.
3. Reconstructing the original cleaned screenplay inputs requires users to obtain source text separately under applicable provider/rightsholder terms.
4. Reliability was measured for the specified Qwen2.5-7B Q4_K_M measurement configuration and should not automatically be generalized to other evaluators.

## Excluded material

- full screenplay text and `script.json`
- raw measurement cache
- raw request telemetry
- local absolute paths
- localhost/server endpoint information
