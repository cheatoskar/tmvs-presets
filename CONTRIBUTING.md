# Contributing

Submit an entry as an issue (the launcher opens a prepared one under *Presets*, *Share mine*) or as a pull request with a new folder. The launcher uploads nothing: you attach the files yourself.

Rules for every entry:

1. It must be your own work, or you have the author's permission and the author is named in the entry. No third-party material without permission, no brand marks or logos in pictures.
2. Name: 1 to 40 characters, none of `\ / : * ? " < > |`, not the name of a built-in preset (Vibrant, Realistic, Golden Hour, Dreamy, Neon, Horizon, Aurora, Competition, Performance, Rainy, Replay Cinema, Storm, Snowstorm, Horror). Folder name (the `id`): a-z, 0-9 and dashes.
3. Description: one or two plain sentences, at most 200 characters. Tags: one to eight from the list in `tools/make-index.py`.
4. Games: only those you tested it in (`tmnf`, `tmuf`, `tmn-eswc`, `tm2`).
5. No advertising and no donation or payment links in names, descriptions or pictures.
6. Nothing that makes the game unplayable (a completely black image, fast flicker). Flashes and flicker go into the description.

Preset (`presets/<id>/`):
- `<id>.ini` at most 16 KB, UTF-8 text, only `[Preset]` and `[Info]` (`Description=`). In `[Preset]` only settings from the *All settings* table of the TMVS docs, values inside their range. Installation settings (video export, render scale, neon trail, VR, game integration) are not allowed; the launcher refuses them.
- `<id>.jpg`: a real JPEG, 16:9, at most 1 MB (384 x 216 is enough). The picture shows the preset, no menu and no player names.
- Easiest: save it in TMVS (*Save as preset*) and take the two files from `Documents\TrackMania\TMVS\presets`.

Look (`luts/<id>/`): `<id>.cube`, 3D, at most 64 x 64 x 64 and 8 MB, input range 0..1 (1D tables and `DOMAIN_MIN`/`DOMAIN_MAX` other than 0/1 do not work). Optional preview `<id>.jpg` (16:9).

Pack (`packs/<id>/`): `<id>.zip` at most 64 MB, only textures and sounds (`.dds`, `.tga`, `.png`, `.jpg`, sounds), nothing executable, no zips inside, no paths with `..`. In `meta.json`: `env` (Stadium, Bay, Coast, Island, Desert, Rally, Snow, Alpine) and only `tmnf`/`tmuf`. A preview in the zip (`Image/LoadScreen.dds` or `preview.png`/`.jpg`) or `<id>.jpg` next to it.

Then run `python tools/make-index.py`: it checks the rules and writes `index.json`.

By submitting you release your preset, look or pack under CC0 (see [LICENSE](LICENSE)).
