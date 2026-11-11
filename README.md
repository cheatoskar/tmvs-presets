# tmvs-presets

**Deutsch**

Das ist meine Sammlung von Presets, Colour-Looks (LUTs) und Resource-Packs für [TM Vibrant Shaders](https://github.com/cheatoskar/TM-Vibrant-Shaders). Launcher und Tools können die `index.json` aus diesem Repo lesen und alles unter *Presets*, *Looks* und *Packs* anzeigen. Installieren heißt: Datei laden, SHA-256 prüfen, Inhalt prüfen, in den Ordner legen, den TMVS beim Spielen liest. Entfernen löscht nur, was der Launcher selbst installiert hat.

Lizenz: Presets, Looks und Packs sind CC0 ([LICENSE](LICENSE)), die Skripte in `tools/` MIT ([tools/LICENSE-MIT](tools/LICENSE-MIT)). Die drei Einträge mit `example` im Namen sind Beispiele für das Format und keine Community-Einträge: sie sind aus den eingebauten Presets Competition, Performance und Horror gemacht, dazu ein Beispiel-Look und ein leeres Beispiel-Pack (nur ein Vorschaubild, es ändert nichts im Spiel).

Aufbau:

| Ordner | Inhalt |
|---|---|
| `presets/<id>/` | `<id>.ini`, `<id>.jpg` (16:9), `meta.json` |
| `luts/<id>/` | `<id>.cube`, optional `<id>.jpg`, `meta.json` |
| `packs/<id>/` | `<id>.zip`, optional `<id>.jpg`, `meta.json` |
| `index.json` | wird von `tools/make-index.py` erzeugt, nicht von Hand ändern |

Index neu bauen und Regeln prüfen: `python tools/make-index.py`. Einreichen: siehe [CONTRIBUTING.md](CONTRIBUTING.md).

**English**

This is my collection of presets, colour looks (LUTs) and resource packs for [TM Vibrant Shaders](https://github.com/cheatoskar/TM-Vibrant-Shaders). Launchers and tools can read `index.json` from this repository and show everything under *Presets*, *Looks* and *Packs*. Installing means: download, check the SHA-256, check the content, write it to the folder TMVS reads while the game runs. Removing deletes only what the launcher installed itself.

Licence: presets, looks and packs are CC0 ([LICENSE](LICENSE)), the scripts in `tools/` are MIT ([tools/LICENSE-MIT](tools/LICENSE-MIT)). The entries with `example` in their name show the format and are not community entries: three are made from the built-in presets Competition, Performance and Horror, plus a sample look and an empty sample pack (only a preview picture, it changes nothing in the game).

Layout: see the table above. Rebuild the index and check the rules with `python tools/make-index.py`. To submit something, read [CONTRIBUTING.md](CONTRIBUTING.md).

## Index format (version 1)

```json
{
  "format": 1,
  "items": [
    {
      "id": "night-drive", "kind": "preset", "name": "Night Drive", "author": "name",
      "description": "One or two sentences.", "tags": ["night", "neon"],
      "games": ["tmnf", "tmuf", "tmn-eswc", "tm2"],
      "files": [
        { "role": "ini", "path": "presets/night-drive/night-drive.ini", "sha256": "<64 hex digits>" },
        { "role": "jpg", "path": "presets/night-drive/night-drive.jpg", "sha256": "<64 hex digits>" }
      ]
    }
  ]
}
```

- `kind`: `preset`, `lut` or `pack`. Files per kind: preset `ini` + `jpg`; lut `cube` (+ optional `preview`); pack `zip` (+ optional `preview`) and `env` (Stadium, Bay, Coast, Island, Desert, Rally, Snow or Alpine).
- `games`: `tmnf`, `tmuf`, `tmn-eswc`, `tm2` (packs: `tmnf`, `tmuf` only).
- `path`: relative to `index.json`, or an https address on the same host. Anything else is refused by the launcher.
- `example: true` marks a sample entry; the launcher shows a badge.
- An entry that breaks a rule is skipped by the launcher, the others stay.

Where the files end up on the player's PC: presets `Documents\TrackMania\TMVS\presets` (Nations, United, ESWC) and `Documents\ManiaPlanet\TMVS\presets` (TM2); looks `...\TMVS\luts`; packs `Documents\TrackMania\Skins\<Environment>\Mod`.
