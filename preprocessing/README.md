# Preprocessing and Corpus Reconstruction

The experimental corpus was aligned against historical STAGE_v0 commit `ce4468eac15775a85e5cd3a2e7255d96ff1afb45`.

## Audited operations

| Film | Operation |
|---|---|
| Chasing Amy | retain first 34 records; remove duplicated second screenplay pass |
| Ghostbusters II | no scene/content cleaning; public experimental serialization has trailing LF |
| The Private Life of Sherlock Holmes | no scene/content cleaning; public experimental serialization has trailing LF |
| Dog Day Afternoon | retain first 69 records; trim duplicated restart material following terminal `THE END` |
| Apocalypse Now | retain first 60 records; trim duplicated restart material following terminal `THE END` |
| Drag Me to Hell | identity |
| Up (2009) | identity |
| Darkman | identity |
| Do the Right Thing | identity |
| The White Ribbon | retain all 76 records; remove non-screenplay IMSDb footer/page material from terminal scene |

The historical total was 1,101 scene records and the cleaned experimental total is 938. The complete 163-record reduction is exactly `34 + 69 + 60` from the three duplicate-pass films.

## Byte-level verification

`scripts/reconstruct_cleaned_corpus.py` serializes each reconstructed JSON using the observed canonical formatting and verifies every output against the SHA-256 recorded in `metadata/source_provenance.csv`. A reconstruction is considered successful only if all ten hashes match.

The script does not obtain screenplay text for the user. Provide a lawful local historical STAGE English directory as input.
