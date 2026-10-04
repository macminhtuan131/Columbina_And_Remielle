# Gemielle — original GIF actions restored

The current ChatGPT pet sheet uses the authored artwork in the repository's
`assets/` folder for its listening, waiting, thinking, writing, and completion
poses. The original GIF files themselves are unchanged.

| ChatGPT pet state | Authoritative source | Behavior |
| --- | --- | --- |
| `idle` (row 0) | `assets/user_typing.gif` | Calmly listens with her clipboard while the user types. |
| `waiting` (row 6) | `assets/waiting_user_input.gif` | Looks expectant with open eyes, waiting for input. |
| `running` (row 7, first three frames) | `assets/ai_thingking.gif` | Thinks with one hand near her chin. |
| `running` (row 7, last three frames) | `assets/ai_typing.gif` | Writes energetically with spiral eyes and her original hand gesture. |
| `review` (row 8) | `assets/ai_complete_answer.gif` | Holds her clipboard up and smiles with closed eyes after completing an answer. |

ChatGPT Pets provides a single active-work animation, so thinking and writing
share one six-frame loop. These images cannot add separate model-thinking or
text-streaming callbacks to the native pet. The happy completion pose follows
the original completion GIF.

Directional movement, waving, jumping, failure, and the sixteen look directions
reuse the previously approved pet rows unchanged. No new artwork was generated.
Source frames were sampled and fitted with one shared scale and a fixed viewport
per authored loop; no individual-frame stretching, redrawing, or recoloring was
used. Cleanup runs with zero color adjustment because these sources already
have transparency.

- [Current v2 sprite sheet](final/spritesheet-extended.png)
- [Web v1 compatibility sheet](final/spritesheet-web-v1.png)
- [All-state animation](final/previews/all-states.gif)
- [Video](final/previews/all-states.mp4)
- [Four behavior stills](final/previews/four-stills.png)
- [Idle → jump → idle](final/previews/idle-jump-idle.gif)
- [Source frame indices and hashes](qa/asset-provenance.json)
- [Quality report](qa/pet-quality.json)
- [Source GIF contact sheet](qa/assets-audit/original-assets-contact-sheet.png)

The previous final artwork and JSON review records are preserved in
`revisions/before-assets-v2/`. The repair sources, frame exports, and reports are
in `revisions/assets-faithful-v2/`.

## Rebuild from the original assets

With Python, Pillow, and the Create Pet skill's bundled scripts available, run:

```powershell
python pet/Gemielle/tools/rebuild_from_assets.py --repo . --skill-dir "<Create Pet skill directory>" --source-atlas pet/Gemielle/revisions/before-assets-v2/final/spritesheet-extended.png --run-dir pet/Gemielle/revisions/assets-faithful-v2
```

The script uses the bundled frame inspection, atlas composition, chroma cleanup,
structural validation, direction review, quality gate, and state preview tools.
The retained rows must remain byte-identical to the previous encoded artwork.
`tools/render_encoded_previews.py` also exports the complete animation, four
stills, jump transition, and look loop directly from the encoded final sheet.
Its optional `--media-path` points to a directory containing `imageio_ffmpeg`
when an MP4 export is needed.

## Account pet identity

The repaired **Gemielle** was created and verified in the connected account on
4 October 2026 (Asia/Saigon), with stable ID
`pet_6ac1b7a1db4881919de940d312e33a52`. See [pet-created.json](pet-created.json).
Select Gemielle in the relevant pet picker to activate her.

The previous creation record and historical ID are preserved in
`revisions/before-assets-v2/pet-created.json`. That historical ID was absent
from the connected account's pet list, so this repair was imported as a new pet
after the user explicitly requested it.
