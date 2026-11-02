# Live2D Production Kit

A Codex skill for creating face-tracked Live2D avatars with Photoshop, Cubism and VTube Studio.

**English** · [简体中文](README.zh-CN.md) · [Releases](https://github.com/Wither033/live2d-production/releases) · [Skill guide](skills/live2d-production/SKILL.md)

## Highlights

- **From portrait to performance.** Plan a character, separate the artwork, build a rig, add motion and connect live face tracking.
- **Start with your existing work.** Continue from a PNG, layered PSD, Cubism project or runtime package.
- **Keep editable sources.** Deliver master artwork, import PSDs, Cubism projects and exported assets for the requested stages.
- **Coordinate desktop production.** Astra directs the workflow; one Terra ultra operator works across Photoshop, Cubism and VTube Studio.
- **Check files with Python.** Inspect PSD structure and runtime references with the included read-only checker.

## Installation

Ask Codex to install the skill:

```text
$skill-installer Install the skill from https://github.com/Wither033/live2d-production/tree/main/skills/live2d-production
```

For a release package, [download the ZIP](https://github.com/Wither033/live2d-production/releases/latest/download/live2d-production.zip) and extract the `live2d-production` folder into `$CODEX_HOME/skills/` (default: `~/.codex/skills/`).

```text
$CODEX_HOME/skills/live2d-production/SKILL.md
```

Invoke the installed skill with `$live2d-production`.

### Setup

| Component | Use |
| --- | --- |
| Windows Codex with native Computer Use | Desktop production |
| Astra (`gpt-6-astra`) | Planning, coordination and review |
| Terra (`gpt-6.1-terra`, `ultra` reasoning) | One desktop operator across the production apps |
| [Adobe Photoshop](https://www.adobe.com/products/photoshop.html) | Artwork separation, hidden-area repair and PSD assembly |
| [Live2D Cubism Editor](https://www.live2d.com/en/cubism/download/editor/) | Meshes, rigging, physics, animation and export |
| VTube Studio | Model setup, parameter mapping and face tracking |
| Webcam or supported phone, with a live performer | Tracking calibration and verification |
| Python 3.9+ | Standalone file checks using the standard library |

Prepare the apps and licenses for your chosen stages. Image generation is used when the task calls for new artwork. Production guides and checker messages are in Chinese.

## Quick start

### Turn a portrait into a layered PSD

Attach your portrait in an Astra session:

```text
Use $live2d-production to turn this portrait into a layered PSD.
Keep the original face and costume, with each full iris behind the eyelids.
Deliver the editable master and the Cubism import PSD.
Finish at the PSD stage.
```

### Continue an editable model

```text
Use $live2d-production with my .cmo3.
Keep my eyelid poses and give the nod a softer return.
Save the updated editable project and export the model.
```

### Set up face tracking

```text
Use $live2d-production with this .model3.json package.
Load it in VTube Studio and set up webcam tracking.
Keep my existing hotkeys and guide me through live calibration.
```

Specify the source file, the details to preserve and the deliverable you want. For mesh and rig edits, provide the editable Cubism project.

## Workflow

| Starting point | Work | Deliverable |
| --- | --- | --- |
| Character brief | [Design and artwork](skills/live2d-production/references/concept-to-master.md) | Movement brief and approved neutral portrait |
| Portrait or separate parts | [Photoshop preparation](skills/live2d-production/references/photoshop-to-psd.md) | Editable master PSD and Cubism import PSD |
| Layered PSD | [Cubism rigging](skills/live2d-production/references/rig-and-motion.md) | Editable `.cmo3` with meshes, deformers, masks and parameter keyforms |
| Editable Cubism project | [Physics and animation](skills/live2d-production/references/rig-and-motion.md#制作可播放动作) | Physics as requested, editable motion sources and `.motion3.json` clips |
| Runtime package | [VTube Studio setup](skills/live2d-production/references/runtime-to-tracking.md) | Model package, parameter mappings, hotkeys and live tracking setup |

The [parts planner](skills/live2d-production/assets/parts-plan.tsv) records each moving piece and the hidden area to paint behind it. The [desktop handoff guide](skills/live2d-production/references/desktop-handoff.md) keeps the current source, saved progress and next step together.

## File checks

From the repository root, replace the example paths with your files:

```sh
# Check a Cubism runtime package
python -X utf8 skills/live2d-production/scripts/preflight.py runtime "export/Mira/Mira.model3.json"

# Check a Cubism import PSD
python -X utf8 skills/live2d-production/scripts/preflight.py psd "art/Mira-import.psd"
```

The checker returns JSON with `ok`, the file path and check results. Exit code `0` means the file check passed; `1` reports a detected error.

| Check | Coverage |
| --- | --- |
| Runtime | Package-relative references, required files, MOC3 signatures, PNG headers and JSON readability |
| PSD | File header, main data sections, RGB mode and 8-bit depth |

### Verify the result

1. **Files:** run the checker and resolve reported paths or format errors.
2. **Artwork and motion:** inspect the PSD layers and color settings, then load the exported model to review eye closure, head turns, neck/collar alignment and motion transitions.
3. **Live tracking:** calibrate in VTube Studio, then test each eye, head movement and mouth opening with the performer.

## Documentation

- [Skill guide](skills/live2d-production/SKILL.md): stage selection, operator roles and delivery rules.
- [Production guides](skills/live2d-production/references/): artwork, Photoshop, Cubism, VTube Studio and desktop handoffs.
- [Parts planner](skills/live2d-production/assets/parts-plan.tsv): movement and hidden-area planning.
- [Preflight source](skills/live2d-production/scripts/preflight.py): standalone structural checks.

## Development

Run the [checker tests](skills/live2d-production/tests/test_preflight.py):

```sh
python -X utf8 -m unittest discover -s skills/live2d-production/tests -p "test_*.py"
```

The test suite uses synthetic PSD and runtime fixtures to exercise file validation.
