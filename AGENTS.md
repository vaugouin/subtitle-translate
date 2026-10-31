# subtitle-translate

Standalone Streamlit application that translates SRT subtitles through the OpenAI SDK.
The canonical task list is in Nestor: `../../Nestor/projets/t2s-backlog/repos/subtitle-translate.md`.

- `app.py` owns upload decoding, translation and subtitle reconstruction.
  `normalize_srt.py` is dependency-free and safe to import; it owns
  `f_split_srt_blocks` (contract in its docstring) and the normalization CLI.
- Do not use the `normalize_srt` file-rewriting CLI as an upload preprocessing
  side effect: the splitter works on decoded text in memory.
- `test-srt-blocks.py` (run command in its docstring) needs no Streamlit,
  credentials or model. Its fixtures are synthetic; never present them as a
  replay of the missing Tarabella file.
- Production runs in Docker (`subtitle-translate.sh`). Local parser tests do not
  establish deployment or translation-model acceptance. Do not deploy, commit or
  push without the relevant user request.
- Follow the parent `../AGENTS.md`. No local application-version convention exists.
