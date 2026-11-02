# 从本次导出的模型到真人面捕

### 从明确的源工程输出

保存本轮 `.cmo3`，在 Cubism 编辑纹理集：遮罩、闭眼线、张口时才显示的部件也要进入运行时，参考整图不要混入。优先保证眼、嘴和发丝的纹理密度；图集页数/尺寸由模型与目标设备决定，不固定写死 4096。

**文件 → 输出嵌入文件 → 输出 MOC3 文件**：选择目标 VTS 支持的稳定 SDK 版本；需要物理时勾选随模型输出物理文件。得到 `.model3.json`、`.moc3` 和纹理 PNG；`.physics3.json` 只在使用物理时需要，`.cdi3.json` 是可选显示信息。动画场景从动画工程导出 `.motion3.json`，需要的表情用 `.exp3.json`。SDK/Viewer 若要按索引播放，在 `FileReferences.Motions` 登记；VTS 的待机/快捷键在其模型配置中设置。[纹理集](https://docs.live2d.com/zh-CHS/cubism-editor-manual/texture-atlas-edit/) · [运行时导出](https://docs.live2d.com/zh-CHS/cubism-editor-manual/export-moc3-motion3-files/) · [VTS 动作](https://github.com/DenchiSoft/VTubeStudio/wiki/Animations)

在技能目录（与 `SKILL.md` 同级）运行只读预检。把示例索引换成包内的实际文件；额外动作路径相对于索引。没有约定物理或动作时省略对应选项：

```powershell
python -X utf8 ./scripts/preflight.py runtime 'D:/Models/角色/角色.model3.json' --expect-physics --motion 'motions/点头.motion3.json'
```

再用对应 Viewer/运行时加载**这一次的包**，看中性外观、已改参数和实际动作。旧运行时的样片可以作为动作预览，不是新版 `.cmo3` 导出或新网格的验收证据。

### 接入 VTube Studio

1. 模型选择 → **Import your own Model → Open folder**，取得用户实际的 `Live2DModels` 路径。不遍历所有 Steam 库。复制**整个导出目录**，保留相对路径；升级先保留现用 `.vtube.json`、录制动作、热键和模型 ID，避免覆盖。需要并排版本时确认模型身份独立。按用户的 Steam 安装/购买分工办事。
2. 加载模型并运行 **Auto Setup**（新模型）。已有个人映射时先保留，不自动重跑覆盖。界面只剩角色时，在空白背景双击显示菜单。模型可见证明加载，不证明摄像头已开。[官方导入](https://github.com/DenchiSoft/VTubeStudio/wiki/Loading-your-own-Models) · [自动设置](https://github.com/DenchiSoft/VTubeStudio/wiki/VTS-Model-Settings)
3. 看输入/输出的实际 ID 和动态指示点，不按镜像画面猜左右。常用映射如下，范围以此模型为准：

| VTS 输入 | 模型输出 | 实看什么 |
| --- | --- | --- |
| `FaceAngleX`、`FaceAngleY`、`FaceAngleZ` | `ParamAngleX`、`ParamAngleY`、`ParamAngleZ` | 自然转头、抬头、倾斜，领口不断开。 |
| EyeOpenLeft、EyeOpenRight | ParamEyeLOpen、ParamEyeROpen | 只闭一眼，另一眼不被硬拉闭。 |
| `EyeLeftX`、`EyeLeftY` 或对应右眼输入 | `ParamEyeBallX`、`ParamEyeBallY` | 视线往四边不露虹膜切边；按实际方向调映射。 |
| MouthOpen | ParamMouthOpenY | 自然闭嘴归零，张嘴中段连续。 |
| 自动呼吸 | ParamBreath | 胸肩起伏，不让头脸伸缩。 |

4. 先校准，再调个别映射。一条轴在端点僵住时看实测输入/输出范围，必要时收窄输出或开该轴 **Limit Range**；平滑越强延迟越大。不要全模型一键降幅。发物理由已登记的物理组驱动，同一输出不再写面捕或普通动作。待机、面捕、单次动作、覆盖型表情、物理的常规优先级逐级升高；Add/Multiply 表情另作叠加。[VTS 优先级](https://github.com/DenchiSoft/VTubeStudio/wiki/Interaction-between-Animations,-Tracking,-Physics,-etc.)
5. 待机设在模型设置里；一次性动作设 **Play Animation** 热键，表情设 **Set/Unset Expression**。播放完试着继续说话/转头，确认控制交回面捕。模型内的开关闭合姿态与整段预制动画不是一回事。

### 真人校准是最后一项，不是文件测试

- **Windows 摄像头**：设置 → 第二页摄像头/跟踪设置 → 选设备 → Tracking Quality。Google Mediapipe 内置，可作为普通摄像头起点；已有兼容 RTX 方案时可比较，不因做技能或接入就安装 DLC。设备支持时从 720p / 30 FPS 开始。由用户处理实际的摄像头许可；**Camera ON → 正常坐姿、自然睁眼闭嘴 → Calibrate**。[摄像头跟踪器](https://github.com/DenchiSoft/VTubeStudio/wiki/Mediapipe-Webcam-Tracker) · [校准](https://github.com/DenchiSoft/VTubeStudio/wiki/Getting-Started#calibrating-the-camera)
- **手机**：在电脑加载模型，手机只传跟踪数据，不必重复装模型；按设备选 USB 或同网连接，用户处理信任/设备许可。[手机到电脑](https://github.com/DenchiSoft/VTubeStudio/wiki/Streaming-to-Mac-PC)
- 单眼眨眼时若总是两眼一起闭，先看 VTS 的 **Link Eye Blinking** 是否主动联动两眼，再区分输入映射与模型绑定。不要先回 Cubism 重画已正确的眼睑。[跟踪设置](https://github.com/DenchiSoft/VTubeStudio/wiki/VTube-Studio-Settings#link-eye-blinking)
- 让镜头前的人分别眨左眼、眨右眼、开闭嘴、左右看、点头/歪头并回正；短暂离开镜头再返回，看模型能否恢复。只把操作者实际看见或本人已明确确认的动作记为通过。没有真人时给出整包、加载方法和待做的校准步骤，不用模拟注入冒充真人。
- 若要视频：VTS **Record Live2D Animation** 保存动作曲线而非视频。可回放并用 OBS 录 MP4；或把录制动作导入 Cubism 的 **60 FPS 场景**再输出视频。录制参数不会自动带回原说话音轨。[VTS 录制说明](https://github.com/DenchiSoft/VTubeStudio/wiki/Record-Animations) · [OBS 捕获](https://github.com/DenchiSoft/VTubeStudio/wiki/Recording-Streaming-with-OBS)
- 程序复制文件不需要 GUI。已经启用且授权的 VTS 官方 WebSocket API 可列出/加载模型、触发现有快捷键或注入输入；不替代摄像头许可、真人校准或 Cubism 建模。[官方 API](https://github.com/DenchiSoft/VTubeStudio#api-details)

交付时把可编辑源（拆分母 PSD、载入 PSD、`.cmo3`、如适用的 `.can3` 或曲线源）与可复制的运行时目录分开。写清从哪份源导出、复制哪个文件夹、怎样启用动作、哪些验收实际完成；不把安装进用户目录说成已经启动并面捕。
