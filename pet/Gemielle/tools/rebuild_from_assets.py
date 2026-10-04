"""Rebuild Gemielle's pet states from the authored assets without redrawing them.

Requires Pillow and the authoritative scripts shipped with the Create Pet skill.
Only crops, samples, scales, and assembles existing authored pixels.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

SPECS = [
    ("idle", 0, 6), ("running-right", 1, 8), ("running-left", 2, 8),
    ("waving", 3, 4), ("jumping", 4, 5), ("failed", 5, 8),
    ("waiting", 6, 6), ("running", 7, 6), ("review", 8, 6),
]
SOURCES = {
    "idle": [("user_typing.gif", i) for i in (0, 10, 20, 30, 40, 50)],
    "waiting": [("waiting_user_input.gif", i) for i in (0, 7, 14, 20, 27, 34)],
    "running": [("ai_thingking.gif", i) for i in (0, 14, 28)]
               + [("ai_typing.gif", i) for i in (0, 6, 12)],
    "review": [("ai_complete_answer.gif", i) for i in (0, 5, 10, 15, 20, 25)],
}

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def execute(skill, name, *args):
    result = subprocess.run(
        [sys.executable, str(skill / name), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8",
    )
    if result.returncode:
        raise RuntimeError(name + "\n" + result.stdout + "\n" + result.stderr)
    print(name + ": passed", flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--skill-dir", type=Path, required=True)
    parser.add_argument("--source-atlas", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    repo, run = args.repo.resolve(), args.run_dir.resolve()
    scripts = args.skill_dir.resolve() / "scripts"
    sys.path.insert(0, str(scripts))
    from assemble_extended_atlas import load_base_rows, paste_look_cells, clear_transparent_rgb
    frames = run / "frames"
    final = run / "final"
    qa = run / "qa"
    final.mkdir(parents=True, exist_ok=True)
    source_atlas = Image.open(args.source_atlas).convert("RGBA")
    assert source_atlas.size == (1536, 2288)

    source_images = {}
    source_bounds = {}
    records = []
    for state, picks in SOURCES.items():
        for name, index in picks:
            with Image.open(repo / "assets" / name) as opened:
                opened.seek(index)
                image = opened.convert("RGBA")
            source_images[name, index] = image
            bbox = image.getbbox()
            bounds = source_bounds.get(name, bbox)
            source_bounds[name] = (
                min(bounds[0], bbox[0]), min(bounds[1], bbox[1]),
                max(bounds[2], bbox[2]), max(bounds[3], bbox[3]),
            )

    # One scale for every GIF. Each authored loop uses one fixed source viewport;
    # no per-frame fitting, centering, pose warping, recoloring, or drawing.
    scale = min(
        176 / max(b[2] - b[0] for b in source_bounds.values()),
        194 / max(b[3] - b[1] for b in source_bounds.values()),
    )
    for state, row, count in SPECS:
        target = frames / state
        target.mkdir(parents=True, exist_ok=True)
        for index in range(count):
            if state in SOURCES:
                name, source_index = SOURCES[state][index]
                bounds = source_bounds[name]
                source = source_images[name, source_index]
                size = (round((bounds[2] - bounds[0]) * scale),
                        round((bounds[3] - bounds[1]) * scale))
                pixels = source.crop(bounds).resize(size, Image.Resampling.LANCZOS)
                cell = Image.new("RGBA", (192, 208), (0, 0, 0, 0))
                cell.alpha_composite(pixels, ((192 - size[0]) // 2, 203 - size[1]))
                records.append({
                    "state": state, "row": row, "frame": index,
                    "source": "assets/" + name, "source_frame": source_index,
                    "source_sha256": hashlib.sha256((repo / "assets" / name).read_bytes()).hexdigest(),
                    "source_viewport": list(bounds), "shared_scale": scale,
                })
            else:
                cell = source_atlas.crop((index * 192, row * 208,
                                          (index + 1) * 192, (row + 1) * 208))
            cell.save(target / (str(index).zfill(2) + ".png"))

    write_json(qa / "asset-provenance.json", {
        "operation": "sample and uniformly fit original GIF pixels; preserve other approved rows",
        "shared_scale": scale, "replaced_rows": [0, 6, 7, 8],
        "preserved_rows": [1, 2, 3, 4, 5, 9, 10],
        "source_atlas_sha256": hashlib.sha256(args.source_atlas.read_bytes()).hexdigest(),
        "frames": records,
        "work_loop": "three authored thinking poses, then three authored writing poses",
    })
    execute(scripts, "inspect_frames.py", "--frames-root", frames,
            "--json-out", qa / "review.json")
    execute(scripts, "compose_atlas.py", "--frames-root", frames,
            "--output", qa / "spritesheet-standard.png")

    # Reuse the approved look cells verbatim using the bundled atlas functions.
    atlas = load_base_rows(qa / "spritesheet-standard.png")
    look_cells = [source_atlas.crop((i % 8 * 192, (9 + i // 8) * 208,
                  (i % 8 + 1) * 192, (10 + i // 8) * 208)) for i in range(16)]
    paste_look_cells(atlas, look_cells)
    clear_transparent_rgb(atlas).save(final / "spritesheet-extended-pre-despill.png")
    execute(scripts, "despill_chroma_edges.py",
            final / "spritesheet-extended-pre-despill.png",
            "--output", final / "spritesheet-extended.png",
            "--chroma-key", "#00FF00", "--strength", "0",
            "--json-out", qa / "chroma-despill-extended.json")
    execute(scripts, "validate_atlas.py", final / "spritesheet-extended.png",
            "--require-v2", "--chroma-key", "#00FF00",
            "--json-out", final / "validation-extended.json")

    # No preserved animation/look pixels may be changed by the rebuild.
    repaired = Image.open(final / "spritesheet-extended.png").convert("RGBA")
    for row in (1, 2, 3, 4, 5, 9, 10):
        box = (0, row * 208, 1536, (row + 1) * 208)
        assert repaired.crop(box).tobytes() == source_atlas.crop(box).tobytes(), row
    repaired.crop((0, 0, 1536, 1872)).save(final / "spritesheet-web-v1.png")
    execute(scripts, "validate_atlas.py", final / "spritesheet-web-v1.png",
            "--chroma-key", "#00FF00", "--json-out", qa / "validation-web-v1.json")
    execute(scripts, "make_contact_sheet.py", final / "spritesheet-extended.png",
            "--output", final / "contact-sheet.png")
    execute(scripts, "make_direction_qa_sheet.py", final / "spritesheet-extended.png",
            "--output", qa / "direction-qa.png")
    execute(scripts, "measure_direction_continuity.py", final / "spritesheet-extended.png",
            "--json-out", qa / "look-continuity.json")
    # Direction semantics are reusable because every look pixel is unchanged.
    shutil.copy2(args.source_atlas.parent.parent / "qa" / "direction-semantics.json",
                 qa / "direction-semantics.json")
    execute(scripts, "validate_pet_quality.py", final / "spritesheet-extended.png",
            "--atlas-validation", final / "validation-extended.json",
            "--chroma-report", qa / "chroma-despill-extended.json",
            "--frame-review", qa / "review.json",
            "--direction-semantics", qa / "direction-semantics.json",
            "--continuity", qa / "look-continuity.json",
            "--json-out", qa / "pet-quality.json")
    # Render from the encoded atlas cells, including its normalized alpha bytes.
    for state, row, count in SPECS:
        for index in range(count):
            repaired.crop((index * 192, row * 208, (index + 1) * 192,
                           (row + 1) * 208)).save(frames / state / (str(index).zfill(2) + ".png"))
    execute(scripts, "render_animation_previews.py",
            "--frames-root", frames, "--output-dir", final / "previews")
    print("Rebuilt original GIF actions; all seven retained rows are byte-identical.", flush=True)

if __name__ == "__main__":
    main()
