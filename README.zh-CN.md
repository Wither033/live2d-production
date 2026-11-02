# Live2D 角色制作工具包

**Live2D Production Kit**：通过 Photoshop、Cubism 和 VTube Studio 制作可面捕角色的 Codex 技能。

[English](README.md) · **简体中文** · [版本发布](https://github.com/Wither033/live2d-production/releases) · [技能指南](skills/live2d-production/SKILL.md)

## 功能亮点

- **从立绘到角色表演。** 串联角色设计、拆件补画、网格绑定、动作制作与真人面捕。
- **接续已有成果。** 从 PNG、分层 PSD、Cubism 工程或运行时包开始，推进当前阶段。
- **保留可编辑源文件。** 按所需阶段交付母档、载入 PSD、Cubism 工程及导出素材。
- **协同操作桌面软件。** Astra 规划与验收，由同一名 Terra ultra 连续操作 Photoshop、Cubism 和 VTube Studio。
- **用 Python 预检文件。** 通过附带的只读脚本检查 PSD 结构与运行时文件引用。

## 安装

把下面这句话发给 Codex：

```text
$skill-installer 安装这个技能：https://github.com/Wither033/live2d-production/tree/main/skills/live2d-production
```

使用发布版本时，[下载技能 ZIP](https://github.com/Wither033/live2d-production/releases/latest/download/live2d-production.zip)，把里面的 `live2d-production` 文件夹解压到 `$CODEX_HOME/skills/`（默认是 `~/.codex/skills/`）。

```text
$CODEX_HOME/skills/live2d-production/SKILL.md
```

安装后使用 `$live2d-production` 调用技能。

### 环境准备

| 组件 | 用途 |
| --- | --- |
| 支持原生 Computer Use 的 Windows Codex | 桌面制作 |
| Astra（`gpt-6-astra`） | 规划、协调与验收 |
| Terra（`gpt-6.1-terra`，`ultra` 推理强度） | 作为唯一桌面操作者接续各软件工序 |
| [Adobe Photoshop 官方产品页](https://www.adobe.com/products/photoshop.html) | 立绘拆件、隐藏区域补画、PSD 组装 |
| [Live2D Cubism Editor 官方下载](https://www.live2d.com/en/cubism/download/editor/) | 网格、绑定、物理、动画与导出 |
| VTube Studio | 模型设置、参数映射与真人面捕 |
| 电脑摄像头或受支持的手机，以及镜头前的表演者 | 面捕校准与验证 |
| Python 3.9+ | 使用标准库独立运行文件预检 |

按所需阶段准备软件及许可证。需要绘制新素材时使用生图能力。制作指南和预检提示均为中文。

## 快速开始

### 把立绘拆成分层 PSD

在 Astra 会话里附上立绘：

```text
用 $live2d-production 把这张立绘拆成分层 PSD。
保留原来的脸和服装，眼睑后方的虹膜保持完整。
交付可编辑母档和 Cubism 载入 PSD。
本次做到 PSD 阶段。
```

### 接续可编辑模型

```text
用 $live2d-production 接着做我的 .cmo3。
保留我调过的眼睑，让点头回正时柔和一点。
保存更新后的可编辑工程并导出模型。
```

### 接入真人面捕

```text
用 $live2d-production 处理这份 .model3.json 运行时包。
载入 VTube Studio，接上电脑摄像头面捕。
保留现有快捷键，并指导我完成真人校准。
```

说明源文件、需要保留的细节和交付终点。修改网格与绑定时，提供对应的可编辑 Cubism 工程。

## 制作流程

| 起点 | 工序 | 交付物 |
| --- | --- | --- |
| 文字设定 | [角色设计与立绘](skills/live2d-production/references/concept-to-master.md) | 动作需求、定稿中性立绘 |
| 立绘或散件 | [Photoshop 拆分](skills/live2d-production/references/photoshop-to-psd.md) | 可编辑母档、Cubism 载入 PSD |
| 分层 PSD | [Cubism 绑定](skills/live2d-production/references/rig-and-motion.md) | 带网格、变形器、剪贴和参数关键形的 `.cmo3` |
| 可编辑 Cubism 工程 | [物理与动画](skills/live2d-production/references/rig-and-motion.md#制作可播放动作) | 按需设置的物理、可编辑动作源、`.motion3.json` |
| 运行时包 | [VTube Studio 配置](skills/live2d-production/references/runtime-to-tracking.md) | 模型整包、参数映射、快捷键与真人面捕配置 |

[部件运动表](skills/live2d-production/assets/parts-plan.tsv)记录每个可动件及其背后需要补画的区域。[桌面交接指南](skills/live2d-production/references/desktop-handoff.md)将当前源文件、已保存进度和下一步集中记录，方便接续。

## 文件预检

在仓库根目录运行，将示例路径替换为自己的文件：

```sh
# 检查 Cubism 运行时包
python -X utf8 skills/live2d-production/scripts/preflight.py runtime "export/Mira/Mira.model3.json"

# 检查 Cubism 载入 PSD
python -X utf8 skills/live2d-production/scripts/preflight.py psd "art/Mira-import.psd"
```

脚本输出包含 `ok`、文件路径和检查结果的 JSON。退出码 `0` 表示文件检查通过，`1` 表示检测到错误。

| 检查项 | 覆盖内容 |
| --- | --- |
| 运行时包 | 包内相对引用、必需文件、MOC3 签名、PNG 文件头、JSON 可读性 |
| PSD | 文件头、主要数据区、RGB 模式、8 位深度 |

### 验收成果

1. **文件：** 运行预检，处理报告中的路径或格式问题。
2. **画面与动作：** 检查 PSD 图层与色彩设置，再试载导出模型，查看闭眼、转头、颈部与衣领衔接、动作过渡。
3. **真人面捕：** 在 VTube Studio 中校准，分别验证左右眼、头部运动和张嘴效果。

## 文档

- [技能指南](skills/live2d-production/SKILL.md)：阶段选择、角色分工与交付规则。
- [制作参考](skills/live2d-production/references/)：立绘、Photoshop、Cubism、VTube Studio 与桌面交接。
- [部件运动表](skills/live2d-production/assets/parts-plan.tsv)：可动件与隐藏区域规划。
- [预检脚本](skills/live2d-production/scripts/preflight.py)：独立文件结构检查。

## 开发

运行[预检测试](skills/live2d-production/tests/test_preflight.py)：

```sh
python -X utf8 -m unittest discover -s skills/live2d-production/tests -p "test_*.py"
```

测试集使用合成 PSD 和运行时样本验证文件检查逻辑。
