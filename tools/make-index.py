"""Builds index.json from the folders in presets/, luts/ and packs/ and checks the submission rules.

Each entry is a folder named after its id (a-z, 0-9, dashes; 2 to 48 characters) with a meta.json:

  presets/<id>/   <id>.ini  <id>.jpg  meta.json     ini <= 16 KB, jpg 16:9 JPEG <= 1 MB
  luts/<id>/      <id>.cube [<id>.jpg]  meta.json   3D .cube up to 64^3 and 8 MB, input range 0..1; optional preview
  packs/<id>/     <id>.zip  [<id>.jpg]  meta.json   environment mod zip <= 64 MB (textures only); optional preview; meta has "env"

  meta.json: {"name", "author", "description", "tags", "games"}  (+ "env" for packs, + "example": true for sample entries)

Run:  python tools/make-index.py          writes index.json and checks the rules
      python tools/make-index.py --check  only checks (exit code 1 on a problem)

The launcher checks the same rules again before it writes a file (known preset keys and ranges, real JPEG, real cube,
zip paths, sha256), so this script is a convenience for contributors and maintainers, not a security boundary.
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES = {"tmnf", "tmuf", "tmn-eswc", "tm2"}
ENVS = {"Stadium", "Bay", "Coast", "Island", "Desert", "Rally", "Snow", "Alpine"}
TAGS = {"day", "sunset", "night", "rain", "snow", "storm", "weather", "realistic", "cinematic", "replay", "neon", "space", "dark",
        "pastel", "clarity", "lightweight", "stylised", "colourful", "vr", "warm", "cold", "film", "bw", "retro", "textures", "sky", "road"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}$")
LIMITS = {"ini": 16 * 1024, "jpg": 1 << 20, "cube": 8 << 20, "zip": 64 << 20}
KINDS = {  # folder -> (kind, required file role/extension, optional preview)
    "presets": ("preset", [("ini", "ini"), ("jpg", "jpg")], False),
    "luts": ("lut", [("cube", "cube")], True),
    "packs": ("pack", [("zip", "zip")], True),
}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    check_only = "--check" in sys.argv
    problems = []
    items = []
    for folder, (kind, required, preview) in KINDS.items():
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        for pid in sorted(os.listdir(base)):
            d = os.path.join(base, pid)
            if not os.path.isdir(d):
                continue
            bad = lambda msg: problems.append(f"{folder}/{pid}: {msg}")
            if not ID_RE.match(pid):
                bad("folder name must be a-z, 0-9 and dashes, 2 to 48 characters")
            meta_path = os.path.join(d, "meta.json")
            if not os.path.isfile(meta_path):
                bad("meta.json is missing")
                continue
            meta = json.load(open(meta_path, encoding="utf-8"))
            files = []
            for role, ext in required:
                p = os.path.join(d, f"{pid}.{ext}")
                if not os.path.isfile(p):
                    bad(f"{pid}.{ext} is missing")
                    continue
                if os.path.getsize(p) > LIMITS[ext]:
                    bad(f"{pid}.{ext} is larger than {LIMITS[ext] // 1024} KB")
                files.append({"role": role, "path": f"{folder}/{pid}/{pid}.{ext}", "sha256": sha(p)})
            pv = os.path.join(d, f"{pid}.jpg")
            if preview and os.path.isfile(pv):
                files.append({"role": "preview", "path": f"{folder}/{pid}/{pid}.jpg", "sha256": sha(pv)})
            for f in files:
                if f["path"].endswith(".jpg"):
                    with open(os.path.join(ROOT, f["path"]), "rb") as fh:
                        if fh.read(3) != b"\xff\xd8\xff":
                            bad("the picture is not a JPEG")
                        if os.path.getsize(os.path.join(ROOT, f["path"])) > LIMITS["jpg"]:
                            bad("the picture is larger than 1 MB")
            name = str(meta.get("name", "")).strip()
            if not (1 <= len(name) <= 40) or re.search(r'[\\/:*?"<>|]', name):
                bad("name: 1 to 40 characters, none of \\ / : * ? \" < > |")
            if not meta.get("author"):
                bad("author is missing")
            if not (1 <= len(str(meta.get("description", ""))) <= 200):
                bad("description: 1 to 200 characters")
            tags = meta.get("tags", [])
            if not tags or len(tags) > 8 or any(t not in TAGS for t in tags):
                bad("tags: one to eight, from " + ", ".join(sorted(TAGS)))
            games = meta.get("games", [])
            if not games or any(g not in GAMES for g in games):
                bad("games: at least one of " + ", ".join(sorted(GAMES)))
            entry = {"id": pid, "kind": kind, "name": name, "author": meta.get("author"), "description": meta.get("description"),
                     "tags": tags, "games": games}
            if kind == "pack":
                if meta.get("env") not in ENVS:
                    bad("env: one of " + ", ".join(sorted(ENVS)))
                if any(g not in ("tmnf", "tmuf") for g in games):
                    bad("packs are for tmnf and tmuf")
                entry["env"] = meta.get("env")
            entry["files"] = files
            if meta.get("example"):
                entry["example"] = True
            items.append(entry)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    if not check_only:
        with open(os.path.join(ROOT, "index.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump({"format": 1, "items": items}, f, indent=1, ensure_ascii=False)
            f.write("\n")
    print(f"{len(items)} entries ok")


if __name__ == "__main__":
    main()
