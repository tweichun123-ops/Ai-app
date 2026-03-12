# Nexis 首登后 AI 形象 + 性格定制 + 通讯式聊天

基于你最新页面，这版后端 demo 支持：

1. 首次登录后进入定制流程。
2. 外观定制：AI 生成 或 上传照片。
3. 性格定制：预设人格 + 自定义补充提示词。
4. 开始聊天时返回“通讯样式 UI 数据”，且对方头像使用“已定制形象”。
5. AI 接口先写死（mock），后续可替换真实 API。

## 1) 外观定制字段映射

- `上传照片` 卡片 → `mode=upload_photo` + `photoUrl`
- `AI 生成` 卡片 → `mode=ai_generate`
- `风格关键词` 标签 → `styleKeywords`
- `补充描述` 文本框 → `customPrompt`

### 接口

`POST /api/users/{user_id}/appearance-customization`

请求（AI 生成）：

```json
{
  "mode": "ai_generate",
  "avatarName": "常青藤学长",
  "styleKeywords": ["阳光帅气", "精英西装"],
  "customPrompt": "深邃眼眸，干净背景"
}
```

请求（上传照片）：

```json
{
  "mode": "upload_photo",
  "avatarName": "常青藤学长",
  "styleKeywords": ["高冷禁欲"],
  "customPrompt": "保留五官特征",
  "photoUrl": "https://cdn.example.com/uploads/user-face-001.jpg"
}
```

## 2) 性格定制字段映射

- 性格卡片（温柔男友/高冷学长/奶狗型/...）→ `presetCode`
- 补充描述 → `customPrompt`

### 接口

`POST /api/users/{user_id}/personality-customization`

```json
{
  "presetCode": "puppy_boy",
  "customPrompt": "多一点撒娇，喜欢叫姐姐"
}
```

## 3) 最终确认定制

`POST /api/users/{user_id}/companion-customization`

```json
{
  "language": "ja-JP",
  "avatarCode": "ivy_senior",
  "personalityTags": ["gentle_kind", "intellectual"]
}
```

该接口会把语言/形象标签定稿，并设置 `onboarding_completed=true`。

## 4) 开始聊天（通讯样式）

### 开始聊天

`POST /api/users/{user_id}/chat/start`

返回：

- `uiMode=communication`
- `layout.style=full-screen-call`
- `companion.imageUrl`：优先使用用户定制形象
  - 上传模式：`uploaded_photo_url`
  - AI 生成模式：`generated_image_url`
  - 都没有时：回落默认 avatar 图
- `todayVocab`：词汇卡片数据
- `messages`：首条欢迎语（含翻译）

### 发送消息

`POST /api/users/{user_id}/chat/messages`

```json
{
  "text": "你今天想教我什么？"
}
```

当前由 `MockChatAIClient` 生成回复（先写死）。

### 获取会话

`GET /api/users/{user_id}/chat/session`

## 5) Mock AI API（先写死）

- 图像：`MockAIImageClient`
- 对话：`MockChatAIClient`

后续替换真实供应商时，可仅替换这两个类。

## 6) 运行

```bash
cd backend
python3 demo_server.py
```

服务地址：`http://localhost:8000`

## 7) APP 主页面 Tab 与 VIP（人民币）

### 主页面 Tab

`GET /api/app/main-tabs`

返回固定 4 个主 Tab：

- 聊天（chat）
- 衣橱（closet）
- 回忆（memories）
- 我的（me）

并给出 VIP 建议入口：`我的 -> VIP`。

### VIP 方案（我的-VIP）

`GET /api/users/{user_id}/vip/plans`

本接口已将价格符号统一改为 **人民币符号 `¥`**（不再使用 `$`）。

示例字段：

```json
{
  "currency": {
    "symbol": "¥",
    "code": "CNY",
    "displayName": "人民币"
  },
  "plans": [
    {
      "name": "初见心动",
      "price": {"symbol": "¥", "value": "59", "period": "/月"}
    }
  ]
}
```


## 8) 衣橱详情页与上身预览（基于已创建形象）

针对你给的衣橱详情页，后端新增以下接口：

### 获取衣橱列表

`GET /api/users/{user_id}/closet/items?tab=all`

- 支持 tab：`all`、`free`、`weekly_new`、`rare`
- 返回每个服装的 `isWearing` 状态（是否已穿戴）

### 选择服装生成上身预览

`POST /api/users/{user_id}/closet/try-on`

```json
{
  "itemCode": "suit_midnight_date"
}
```

服务端会基于已创建形象生成试穿预览（当前 mock）：

- 先解析人物底图：
  - 上传照片优先
  - 其次 AI 生成图
  - 否则默认 avatar
- 与所选服装素材合成，返回 `previewImageUrl`

### 获取最近一次试穿预览

`GET /api/users/{user_id}/closet/preview`

### 确认穿戴

`POST /api/users/{user_id}/closet/wear`

```json
{
  "itemCode": "suit_midnight_date"
}
```

用于将该服装标记为当前穿戴，衣橱列表会同步显示 `isWearing=true`。


## 9) 语言学习核心：MCP 风格实时通话交互（Demo）

你提到的核心诉求是：**通话中实时与大模型交互，并实时整理常见词汇/俚语**。这版 demo 提供了可落地的后端接口形态（先 mock，后续替换真实 MCP/Realtime LLM）。

### 9.1 开始实时通话

`POST /api/users/{user_id}/call/start`

返回里会包含：

- `mcp.provider/model/transport`（模拟 MCP 接入信息）
- `learningLanguage`（跟随当前形象语言）
- `companion.imageUrl`（当前形象图）

### 9.2 实时上传语音转写并获取 AI 回合

`POST /api/users/{user_id}/call/stream-turn`

```json
{
  "transcript": "今天学到一个词 kawaii",
  "isFinal": true
}
```

返回：

- `assistantDelta`：AI 实时回复文本（demo 模拟）
- `newVocab`：该回合识别出的词汇/俚语（如 `kawaii`, `rizz`, `lit`）
- `turn`：本轮回合记录

### 9.3 获取通话会话与词汇总结

- `GET /api/users/{user_id}/call/session`
- `GET /api/users/{user_id}/call/vocab-summary`

`vocab-summary` 会去重聚合整场通话的高频词/俚语，方便前端做“今日学习卡片”。

### 9.4 结束通话

`POST /api/users/{user_id}/call/end`

### 9.5 如何接入真实 MCP/Realtime LLM（后续）

当前 demo 的 `MockMCPRealtimeLLM` 是占位实现。替换真实能力时，建议：

1. 将 `infer_reply` 替换为真实实时模型流式推理。
2. 将 `extract_vocab` 替换为：
   - 规则 + 词典 + 小模型分类
   - 或单独调用结构化抽取模型输出 JSON。
3. 在 `stream-turn` 里增加 token streaming（SSE / WebSocket）。
4. 在 `vocabTimeline` 中追加难度、词性、例句、收藏状态等字段。
