# Live2D Production

**English** · [简体中文](README.zh-CN.md)

Start with a character portrait. Separate the parts in Photoshop, rig a blink and a head turn in Live2D Cubism, then drive the model with your face in VTube Studio. If you already have a layered PSD, an editable Cubism project or an exported model, pick up from there.

`$live2d-production` is a Codex skill. Astra directs the work; one Terra ultra operator handles the desktop across all three apps. You can ask for the whole model or stop at a specific deliverable, such as a PSD ready to rig.

## Install

Paste this into Codex:

```text
$skill-installer Install the skill from https://github.com/Wither033/live2d-production/tree/main/skills/live2d-production
```

Or [download the skill ZIP](https://github.com/Wither033/live2d-production/releases/latest/download/live2d-production.zip) and extract the `live2d-production` folder into `$CODEX_HOME/skills/` (default: `~/.codex/skills/`). The file directly inside that folder should be [`SKILL.md`](skills/live2d-production/SKILL.md).

For desktop work, use a Windows Codex session with Astra (`gpt-6-astra`), Terra (`gpt-6.1-terra` at `ultra` reasoning), native Computer Use and the apps needed for your stage. Image generation is only needed when you want new art. Live face tracking needs a webcam or a supported phone and someone in front of it. The operating guides and checker messages are in Chinese.

## Try it with one PNG

Attach your portrait in an Astra session and ask:

> Use `$live2d-production` to turn this portrait into a layered PSD. Keep the original face and costume. Preserve each full iris behind the eyelids so the eyes can look around. Give me the editable master and the Cubism import PSD; stop before rigging.

If you have moved past artwork, name your starting file and the result you want:

- **Editable model:** “Use `$live2d-production` with my `.cmo3`. Keep my eyelid poses. Give the nod a softer return and export the updated model.”
- **Runtime package:** “Use `$live2d-production` with this `.model3.json` export. Load it in VTube Studio and set up webcam tracking. Keep my existing hotkeys.”

## What each stage delivers

| Stage | Deliverable | What to look for |
| --- | --- | --- |
| [Character and artwork](skills/live2d-production/references/concept-to-master.md) | A movement brief and an approved neutral portrait | The face, silhouette and costume still match the design. Approved artwork can go straight to separation. |
| [Photoshop](skills/live2d-production/references/photoshop-to-psd.md) | An editable master PSD and a separate Cubism import PSD | Move the fringe aside: the head underneath should be painted. Put it back: the neutral pose should match the portrait. |
| [Cubism rig](skills/live2d-production/references/rig-and-motion.md) | An editable `.cmo3` with meshes, deformers, masks and parameter keyforms | The eyelids close without flattening the iris; the neck stays inside the collar as the head turns. |
| [Physics and motion](skills/live2d-production/references/rig-and-motion.md#制作可播放动作) | Physics where needed, editable motion sources and exported `.motion3.json` clips | An idle loops without a jump. A one-shot gesture releases its parameters so tracking can take over again. |
| [VTube Studio](skills/live2d-production/references/runtime-to-tracking.md) | A runtime package, parameter mappings, hotkeys and a tracking setup | Blink each eye, turn your head and open your mouth on camera. Loading the model alone doesn’t test tracking. |

The [parts planner](skills/live2d-production/assets/parts-plan.tsv) connects each moving piece to the area you need to paint behind it. The [desktop handoff guide](skills/live2d-production/references/desktop-handoff.md) explains how to resume from a saved file without two operators editing the same model.

## Check an export without opening Cubism

From the repository root, point the [read-only checker](skills/live2d-production/scripts/preflight.py) at your model index. It uses Python 3.9+ and the standard library:

```sh
python -X utf8 skills/live2d-production/scripts/preflight.py runtime "export/Mira/Mira.model3.json"
```

It returns JSON. If a motion file is missing, the error names the motion group, entry and path. To inspect an import PSD instead, use `psd` in place of `runtime` and pass the PSD path. Use the checker for file structure; use the exported model to judge motion and the live camera to judge tracking.
