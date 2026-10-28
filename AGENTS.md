# subtitle-translate

Standalone Streamlit application that translates SRT subtitles through the OpenAI SDK.
The canonical task list is in Nestor: `../../Nestor/projets/t2s-backlog/repos/subtitle-translate.md`.

- `app.py` owns upload decoding, translation and subtitle reconstruction.
- `normalize_srt.py` is dependency-free and safe to import. It owns
  `f_split_srt_blocks`, used by the app, and the existing normalization CLI.
- `test-srt-blocks.py` exercises the real splitter without importing Streamlit,
  reading credentials or calling a model. Run from this directory:
  `uv run --no-project python -B test-srt-blocks.py`.
- Default SRT splitting must accept LF, CRLF, lone CR, a leading Unicode BOM and
  blank separator lines containing spaces/tabs. Preserve cue identifiers,
  timestamps, Unicode, markup and multiline dialogue. The app's chunk size is
  measured in characters; keep an oversized cue intact. Retain custom-separator
  and larger-chunk grouping behavior.
- Do not use the broader `normalize_srt` file-rewriting CLI as an upload
  preprocessing side effect. The splitter operates on decoded text in memory.
- The original Tarabella reproducer is not present. Regression fixtures are
  synthetic Cyrillic subtitles; do not describe them as a replay of that file.
- Production runs in Docker. `subtitle-translate.sh` invokes
  `docker compose up -d --build`. Local parser tests do not establish
  deployment or translation-model acceptance. Do not deploy, commit or push
  without the relevant user request.
- Follow the parent `../AGENTS.md`. Keep project instructions here;
  `CLAUDE.md` is only a pointer. No local application-version convention exists.
