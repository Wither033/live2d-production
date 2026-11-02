# Live2D 角色制作与面捕

[English](README.md) · **简体中文**

从一张角色立绘开始：在 Photoshop 里拆出可动部件，在 Live2D Cubism 里做出眨眼和转头，最后让 VTube Studio 里的角色跟着你的脸动。手上已经有分层 PSD、Cubism 工程或导出包，也可以从那里接着做。

`$live2d-production` 是一个 Codex 技能。Astra 决定怎么做、做到哪一步；同一名 Terra ultra 连续操作三款桌面软件。你可以委托整套模型，也可以只拿一份可以开始绑定的 PSD。

## 安装

把下面这句话发给 Codex：

```text
$skill-installer 安装这个技能：https://github.com/Wither033/live2d-production/tree/main/skills/live2d-production
```

也可以[下载技能 ZIP](https://github.com/Wither033/live2d-production/releases/latest/download/live2d-production.zip)，把里面的 `live2d-production` 文件夹解压到 `$CODEX_HOME/skills/`（默认是 `~/.codex/skills/`）。打开该文件夹，第一层就应当能看到 [`SKILL.md`](skills/live2d-production/SKILL.md)。

桌面制作需要 Windows 版 Codex 可调用 Astra（`gpt-6-astra`）、Terra（`gpt-6.1-terra`，推理强度 `ultra`）及原生 Computer Use，并已安装本阶段要用的软件。需要画新素材时才用生图；真人面捕需要电脑摄像头或受支持的手机，以及镜头前的表演者。操作指南和预检提示均为中文。

## 拿一张 PNG 试试

在 Astra 会话里附上立绘，直接说：

> 用 `$live2d-production` 把这张立绘拆成分层 PSD。保留原来的脸和服装；眼睑后方的虹膜要完整，之后眼珠还要移动。交付可编辑母档和 Cubism 载入 PSD，到这里就停，不开始绑定。

如果立绘已经拆好了，点名现有文件和需要的结果即可：

- **已有可编辑模型：**“用 `$live2d-production` 接着做我的 `.cmo3`。保留我调过的眼睑，让点头回正时柔和一点，再导出更新后的模型。”
- **已有运行时包：**“用 `$live2d-production` 把这份 `.model3.json` 导出包载入 VTube Studio，接上电脑摄像头面捕，保留我原来的快捷键。”

## 每一步拿到什么

| 阶段 | 交付物 | 怎么看效果 |
| --- | --- | --- |
| [角色设定与立绘](skills/live2d-production/references/concept-to-master.md) | 动作需求、定稿的中性立绘 | 脸型、轮廓和服装仍符合设定。已有定稿就直接拆，不重新生图。 |
| [Photoshop 拆分](skills/live2d-production/references/photoshop-to-psd.md) | 可编辑的拆分母档、单独的 Cubism 载入 PSD | 移开刘海，下面该露出的部分已经补全；放回原位，仍与立绘贴合。 |
| [Cubism 网格与绑定](skills/live2d-production/references/rig-and-motion.md) | 带网格、变形器、剪贴和参数关键形的 `.cmo3` | 闭眼时是眼睑合拢，不是虹膜被压扁；转头时脖子不脱离衣领。 |
| [物理与动作](skills/live2d-production/references/rig-and-motion.md#制作可播放动作) | 按需设置的物理、可编辑动作源和导出的 `.motion3.json` | 待机循环首尾不跳；点头等单次动作结束后，面捕能重新接管相应参数。 |
| [VTube Studio 面捕](skills/live2d-production/references/runtime-to-tracking.md) | 运行时整包、参数映射、动作快捷键与面捕配置 | 对着镜头分别眨左右眼、转头、张嘴。仅仅载入模型不能确认真人跟踪效果。 |

[部件运动表](skills/live2d-production/assets/parts-plan.tsv)把“哪一件要动”和“它后面要补什么”放在同一行。[桌面交接指南](skills/live2d-production/references/desktop-handoff.md)说明如何从已保存的文件接续，避免两个人同时改同一个模型。

## 不开 Cubism，也能先查导出包缺了什么

在仓库根目录，把下面的路径换成自己的模型索引。[只读预检脚本](skills/live2d-production/scripts/preflight.py)只需 Python 3.9+，不用安装第三方库：

```sh
python -X utf8 skills/live2d-production/scripts/preflight.py runtime "export/Mira/Mira.model3.json"
```

脚本输出 JSON。比如少了一个动作文件，报错会指出动作组、组内序号和文件路径。要查载入 PSD，就把 `runtime` 改成 `psd`，并传入 PSD 路径。文件结构用脚本查，动作流畅度看实际导出的模型，面捕效果用真人试。
