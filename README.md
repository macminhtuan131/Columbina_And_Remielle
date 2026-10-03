# Columbina & Gemielle — Dreamy trying to develop them

First word from the creator: I tried ._. But I'm still developing them

This repository contains **Gemielle**, a Chrome extension that displays an animated assistant on **Google Gemini** and **ChatGPT**, plus ready-made **Gemielle** and **Columbina** sprite sheets for ChatGPT Pets.

The original Vietnamese installation guide is preserved in [README.vi.md](README.vi.md).

## Meet the characters

| Character | Appearance and mood | Files |
| --- | --- | --- |
| **Gemielle** | A cheerful seated (VOIDHUNTER) chibi assistant with pink hair, large pink eyes, tiny white wings, a white/lavender outfit, and a clipboard. | Browser GIFs in [assets/](assets/); pet artwork in [pet/Gemielle/](pet/Gemielle/). |
| **Columbina** | A gentle seated (Moon Maiden) chibi companion with long burgundy hair, white feather ornaments, blue/white clothing, a white geometric eye mask. | Artwork, revisions, previews, and QA in [pet/Columbina-Chibi/](pet/Columbina-Chibi/). |

| Gemielle | Columbina |
| :---: | :---: |
| ![Gemielle resting](pet/Gemielle/final/previews/idle.png) | ![Columbina resting](pet/Columbina-Chibi/final/previews/idle.png) |

[Watch Gemielle's animations](pet/Gemielle/final/previews/all-states.gif) · [Watch Columbina's animations](pet/Columbina-Chibi/final/previews/all-states.gif) · [Columbina video](pet/Columbina-Chibi/final/previews/all-states.mp4)

## Choose how to use them

| Goal | Method |
| --- | --- |
| Show an animated assistant inside Gemini or ChatGPT in Chrome | Install this repository as an unpacked browser extension. It uses Gemielle by default. |
| Use Columbina's artwork in the browser widget | Make a separate copy of the extension and replace its five GIF assets using the mapping below. There is currently no character picker. |
| Create a native animated companion in ChatGPT Work | Import one of the finished pet sprite sheets through a Pets-enabled workflow. |
| Change the assistant's writing style or persona | Supply separate chat instructions. The extension and pet artwork only affect the visual companion. |

## Install on Gemini and ChatGPT

1. Download this repository as a ZIP and extract it, or clone it.
2. Keep the extracted folder in a permanent location.
3. Open Chrome's extension manager by entering `chrome://extensions/` in the address bar.
4. Enable **Developer mode**, then choose **Load unpacked**.
5. Select the repository's **root folder containing `manifest.json`**. Do not select `assets/` or either pet folder.
6. Open or refresh [Gemini](https://gemini.google.com/) or [ChatGPT](https://chatgpt.com/).

The installed extension is named **Gemielle**, version **1.2**, in the current manifest. It needs no build step, API key, or separate server.

The widget starts near the bottom-right corner. Drag it with the left mouse button to move it. Its position is not saved across page reloads.

### Browser widget states

| State | GIF | Meaning |
| --- | --- | --- |
| `WAITING` | [waiting_user_input.gif](assets/waiting_user_input.gif) | Waiting for a prompt. |
| `USER_TYPING` | [user_typing.gif](assets/user_typing.gif) | You are typing or pasting into an input. |
| `AI_THINKING` | [ai_thingking.gif](assets/ai_thingking.gif) | A request has been submitted and the page is processing it. |
| `AI_TYPING` | [ai_typing.gif](assets/ai_typing.gif) | The adapter detects generated text or image content. |
| `AI_COMPLETE` | [ai_complete_answer.gif](assets/ai_complete_answer.gif) | The adapter detects a finished response. |

The filename `ai_thingking.gif` intentionally keeps its existing spelling because the widget references it directly.

The adapters estimate status from page input events, DOM changes, and generation indicators. Gemini and ChatGPT page changes can affect detection; this is a visual status estimate, not access to the model's internal reasoning.

### Use Columbina in the browser widget

Make a separate copy of the extension folder so you can keep the original Gemielle assets. In that copy, use these existing preview GIFs as replacements:

| Columbina source in `pet/Columbina-Chibi/final/previews/` | Replace file in `assets/` | Suggested visual |
| --- | --- | --- |
| `waiting.gif` | `waiting_user_input.gif` | Expectant waiting. |
| `idle.gif` | `user_typing.gif` | Calmly accompanying your typing. |
| `running.gif` | `ai_thingking.gif` | Active task work. |
| `running.gif` | `ai_typing.gif` | Active task work during generation. |
| `review.gif` | `ai_complete_answer.gif` | Reviewing the completed result. |

Copy each source GIF under the destination filename, reload the extension in Chrome, and refresh the Gemini/ChatGPT tab. These are suggested mappings between the pet's nine states and the widget's five states; the pet has no dedicated `USER_TYPING` animation.

Use the GIFs for this widget. A complete sprite-sheet PNG cannot replace a GIF directly because `core/widget.js` displays ordinary images and does not animate atlas cells.

## Create a ChatGPT pet from this folder

A native ChatGPT pet uses a **transparent sprite sheet**, with the app choosing the animation state. Installing the browser extension does not automatically import the pet.

### Ready-to-use sprite sheets

| Character | Extended v2 sheet — nine states + sixteen look directions | Web v1 compatibility sheet — nine states |
| --- | --- | --- |
| **Columbina** | [spritesheet-extended.png](pet/Columbina-Chibi/final/spritesheet-extended.png) | [spritesheet-web-v1.png](pet/Columbina-Chibi/final/spritesheet-web-v1.png) |
| **Gemielle** | [spritesheet-extended.png](pet/Gemielle/final/spritesheet-extended.png) | [spritesheet-web-v1.png](pet/Gemielle/final/spritesheet-web-v1.png) |

The v2 files are **1536 × 2288**, arranged as **8 columns × 11 rows**, with **192 × 208** cells. The v1 exports are **1536 × 1872** and preserve the exact first nine rows of each finished v2 sheet. They omit the sixteen look directions. Both v1 exports passed the connected Pets validator; their reports are saved in each character's `qa/validation-web-v1.json`.

The connected Pets tools validated Columbina's v2 sheet during this import. Public [ChatGPT Pets documentation](https://learn.chatgpt.com/docs/pets) currently describes a web uploader accepting v1 dimensions; use the v1 export if that is what your uploader requires. Account and workspace availability can differ.

### Import the existing Columbina artwork

In a ChatGPT Work chat with the Pets plugin and access to the file, attach or reference the **finished v2 sprite sheet**, then send:

> Create a new ChatGPT pet named **Columbina** from this attached sprite sheet. Reuse the existing artwork and animations. Validate the sheet before uploading, create the pet, and verify that it appears in my pet list.

For a local chat with folder access, the relative file is:

```text
pet/Columbina-Chibi/final/spritesheet-extended.png
```

A web chat cannot read a local path merely because it appears in your message; attach the file there. For Gemielle, use her corresponding finished file and request the name **Gemielle**.

The import workflow is: **validate the exact file → prepare its upload → create the pet → verify its stable ID**. Select the pet afterward if you want it active. Upload the finished sheet, rather than a contact sheet, reference image, or preview GIF.

### Select or create through ChatGPT's interface

- **Desktop:** open **Settings → Pets**. Select your pet, then use `/pet` or **Show pet** to display the companion. If creating through the interface, choose **Create pet**, provide the artwork in the opened chat, and afterward refresh the pet list. See [official desktop pet instructions](https://learn.chatgpt.com/docs/pets).
- **Web, where available:** open **Settings → Personalization → Pet → Select pet**, then use **Upload pet** for a custom sprite sheet. Use the v1 compatibility PNG if the uploader requires **1536 × 1872**. Native web pets appear in supported Work chats; the browser extension above provides the widget on ordinary ChatGPT and Gemini pages. See [official web pet instructions](https://learn.chatgpt.com/docs/pets).

Desktop pets and web pets have separate interface behavior and may not sync automatically. The Pets-enabled workflow used for this repository can accept the extended v2 format.

### Columbina import record

A new custom pet named **Columbina** was created and verified in the connected Pets account on **4 October 2026** (Asia/Saigon).

- Stable pet ID: `pet_6ac148e303088191917233b149adc538`.
- Source: `pet/Columbina-Chibi/final/spritesheet-extended.png`.
- Artwork SHA-256: `067b8791e19d592d87413e661cec03959ce791f0856700a1a0200d8ad05f1d08`.
- Record: [pet-imported-columbina.json](pet/Columbina-Chibi/pet-imported-columbina.json).

The older **Columbina Chibi** records describe a previous creation/update. Pet IDs belong to the account that created them; other users should import the artwork into their own account.

## Pet animation layout

Rows and frames are zero-indexed. Fill the first indicated number of cells; leave unused cells fully transparent.

| Row | State | Frames |
| --- | --- | ---: |
| 0 | `idle` — calm resting | 6 |
| 1 | `running-right` — rightward movement | 8 |
| 2 | `running-left` — leftward movement | 8 |
| 3 | `waving` — greeting | 4 |
| 4 | `jumping` — vertical jump | 5 |
| 5 | `failed` — blocked/failure reaction | 8 |
| 6 | `waiting` — needs input | 6 |
| 7 | `running` — active work/processing | 6 |
| 8 | `review` — inspecting completed output | 6 |
| 9 | Look directions, up clockwise through down-right | 8 |
| 10 | Look directions, down clockwise through up-left | 8 |

Rows 9–10 belong only to v2. They contain sixteen directions at 22.5° intervals: up = 0°, screen-right = 90°, down = 180°, screen-left = 270°. The `running` work animation is distinct from the two directional movement animations.

For a new design, ask a Pets-enabled creation chat to generate and validate the full animation set. Renaming a single image or GIF as a sprite sheet does not create a usable pet.

## Files and troubleshooting

- [manifest.json](manifest.json): supported websites and extension resource loading.
- [core/widget.js](core/widget.js): the shared widget, GIF mapping, dragging, and state API.
- [adapters/gemini.js](adapters/gemini.js) and [adapters/chatgpt.js](adapters/chatgpt.js): site-specific status detection.
- [style.css](style.css): widget size and appearance.
- `pet/<character>/decoded/`: source strips; `final/`: finished artwork and previews; `qa/`: validation/review reports.
- [Columbina artwork notes](pet/Columbina-Chibi/README.md): previous artwork revisions and preserved character constraints.

**Widget missing:** verify that the extension is enabled, the selected folder contains the manifest, and the tab is on a supported domain. Refresh the tab after loading or reloading the extension.

**State stuck or inaccurate:** try a fresh chat and refresh the page. Detection depends on the website DOM; both adapters have a two-minute safety timeout for active detection. Report the affected website and action if its layout has changed.

**Pet upload rejected:** check the required v1/v2 dimensions, transparency, file size (at most 20 MiB), row counts, and unused cells. Submit the final PNG/WebP, not a preview/contact sheet.

**Pet exists but is not visible:** refresh the relevant pet picker and select it. In the desktop app, also use **Show pet**; reduced-motion settings may display a still frame.

## Privacy and license

The current extension runs in the browser. Its source observes page input and response content to estimate status; it contains no analytics, external API calls, or conversation-storage code.

This is a personal project and is not officially affiliated with Google or OpenAI. See [LICENSE](LICENSE) for the repository's Apache License 2.0 terms. Character artwork and third-party designs may have separate rights.
