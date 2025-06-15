# AIプラットフォームの テキスト生成モデル・埋め込みモデル 詳細仕様レポート

## 1. OpenAI API

### テキスト生成モデル（Completion）

| モデル名 | モデルファミリ | 最大コンテキスト | 価格（USD/1Mトークン） | ストリーミング | ファインチューニング | 主要機能 | ドキュメント |
|---------|-------------|------------------|----------------------|---------------|---------------------|----------|-------------|
| `gpt-4.1` | GPT-4.1 | 1,047,576 | 入力: $2.00<br>出力: $8.00<br>キャッシュ: $0.50 | ◯ | ◯ | Function Calling, Structured Outputs, 画像入力 | [OpenAI Platform](https://platform.openai.com/docs/models/gpt-4.1) |
| `gpt-4.1-mini` | GPT-4.1 | 不明 | 入力: $0.50<br>出力: $2.00<br>キャッシュ: $0.10 | ◯ | ◯ | Function Calling, Structured Outputs | [OpenAI Platform](https://platform.openai.com/docs/models) |
| `gpt-4.1-nano` | GPT-4.1 | 不明 | 入力: $0.20<br>出力: $0.40<br>キャッシュ: $0.025 | ◯ | ◯ | 低遅延タスク最適化 | [OpenAI Platform](https://platform.openai.com/docs/models) |
| `gpt-4o` | GPT-4o | 128,000 | 入力: $2.50<br>出力: $10.00<br>キャッシュ: $1.25 | ◯ | ◯ | マルチモーダル（テキスト、画像、音声） | [OpenAI Platform](https://platform.openai.com/docs/models/gpt-4o) |
| `gpt-4o-mini` | GPT-4o | 128,000 | 入力: $0.15<br>出力: $0.60 | ◯ | ◯ | コスト効率重視モデル | [OpenAI Platform](https://platform.openai.com/docs/models) |

### 埋め込みモデル（Embedding）

| モデル名 | ベクトル次元 | 最大コンテキスト | 価格（USD/1Mトークン） | 機能 | ドキュメント |
|---------|-------------|------------------|----------------------|------|-------------|
| `text-embedding-3-large` | 3,072 | 8,191 | $0.13 | 次元数調整可能、最高性能 | [OpenAI Platform](https://platform.openai.com/docs/models/text-embedding-3-large) |
| `text-embedding-3-small` | 1,536 | 8,191 | $0.02 | 次元数調整可能、コスト効率 | [OpenAI Platform](https://platform.openai.com/docs/models/text-embedding-3-small) |
| `text-embedding-ada-002` | 1,536 | 8,191 | $0.10 | 旧世代モデル（非推奨） | [OpenAI Platform](https://platform.openai.com/docs/models) |

**調査元URL：** [OpenAI API Pricing](https://openai.com/api/pricing/), [New Embedding Models](https://openai.com/index/new-embedding-models-and-api-updates/), 2024年4月更新

---

## 2. Google Gemini API

### テキスト生成モデル（Completion）

| モデル名 | モデルファミリ | 最大コンテキスト | 価格（USD/1Mトークン） | ストリーミング | ファインチューニング | 主要機能 | ドキュメント |
|---------|-------------|------------------|----------------------|---------------|---------------------|----------|-------------|
| `gemini-2.5-flash-preview-04-17` | Gemini 2.5 | 1,048,576 | 無料 / 入力: $0.15<br>出力: $0.60（通常）<br>$3.50（思考） | ◯ | × | 適応的思考、ツール使用、マルチモーダル | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `gemini-2.5-pro-preview-03-25` | Gemini 2.5 | 1,048,576 | 入力: $1.25-2.50<br>出力: $10.00-15.00 | ◯ | × | 高度な推論、大規模データ分析 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `gemini-2.0-flash` | Gemini 2.0 | 1,048,576 | 無料 / 入力: $0.10<br>出力: $0.40 | ◯ | × | 次世代機能、マルチモーダル生成 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `gemini-2.0-flash-lite` | Gemini 2.0 | 1,048,576 | 無料 / 入力: $0.075<br>出力: $0.30 | ◯ | × | コスト効率、低遅延 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `gemini-1.5-flash` | Gemini 1.5 | 1,048,576 | 無料 / 入力: $0.075-0.15<br>出力: $0.30-0.60 | ◯ | ◯ | 汎用性、高速処理 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `gemini-1.5-pro` | Gemini 1.5 | 2,097,152 | 無料 / 入力: $1.25-2.50<br>出力: $5.00-10.00 | ◯ | × | 複雑な推論、2M トークン | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |

### 埋め込みモデル（Embedding）

| モデル名 | ベクトル次元 | 最大コンテキスト | 価格（USD/1Mトークン） | 機能 | ドキュメント |
|---------|-------------|------------------|----------------------|------|-------------|
| `gemini-embedding-exp-03-07` | 3,072 | 8,192 | 無料 | 実験版、SOTA性能 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `text-embedding-004` | 768 | 2,048 | 無料 | 最新世代、高性能 | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |
| `embedding-001` | 768 | 2,048 | 無料 | 標準モデル | [Gemini API](https://ai.google.dev/gemini-api/docs/models) |

**調査元URL：** [Gemini API Models](https://ai.google.dev/gemini-api/docs/models), [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing), 2024年4月更新

---

## 3. Ollama CLI（ローカル／リモートモデル）

### テキスト生成モデル（Completion）

| モデル名 | モデルファミリ | パラメータ数 | コンテキスト長 | 価格 | 主要機能 | ダウンロード |
|---------|-------------|-------------|----------------|------|----------|-------------|
| `deepseek-r1` | DeepSeek-R1 | 1.5B-671B | モデル依存 | 無料 | 推論モデル | [Ollama](https://ollama.com/library/deepseek-r1) |
| `llama4` | Llama 4 | 16x17B-128x17B | 不明 | 無料 | 最新マルチモーダル | [Ollama](https://ollama.com/library/llama4) |
| `llama3.3` | Llama 3.3 | 70B | 不明 | 無料 | 高性能、ツール使用 | [Ollama](https://ollama.com/library/llama3.3) |
| `llama3.1` | Llama 3.1 | 8B-405B | 128K-200K | 無料 | ツール使用、多言語 | [Ollama](https://ollama.com/library/llama3.1) |
| `gemma3` | Gemma 3 | 1B-27B | 不明 | 無料 | Google製、ビジョン対応 | [Ollama](https://ollama.com/library/gemma3) |
| `qwen3` | Qwen 3 | 0.6B-235B | 不明 | 無料 | 中国語・多言語対応 | [Ollama](https://ollama.com/library/qwen3) |
| `mistral` | Mistral | 7B | 32K | 無料 | Apache ライセンス | [Ollama](https://ollama.com/library/mistral) |
|  `phi4` | Phi-4 | 14B | 不明 | 無料 | Microsoft製 | [Ollama](https://ollama.com/library/phi4) |

### 埋め込みモデル（Embedding）

| モデル名 | パラメータ数 | ベクトル次元 | コンテキスト長 | 価格 | 性能 | ダウンロード |
|---------|-------------|-------------|----------------|------|------|-------------|
| `mxbai-embed-large` | 335M | 1024 | 512 | 無料 | SOTA（OpenAI超え） | [Ollama](https://ollama.com/library/mxbai-embed-large) |
| `nomic-embed-text` | 137M | 768 | 8192 | 無料 | 長文対応、高性能 | [Ollama](https://ollama.com/library/nomic-embed-text) |
| `all-minilm` | 23M-33M | 384 | 256 | 無料 | 軽量、汎用 | [Ollama](https://ollama.com/library/all-minilm) |
| `bge-m3` | 567M | 1024 | 8192 | 無料 | 多機能、多言語 | [Ollama](https://ollama.com/library/bge-m3) |
| `snowflake-arctic-embed` | 22M-335M | 384-1024 | 512 | 無料 | Snowflake製 | [Ollama](https://ollama.com/library/snowflake-arctic-embed) |

**調査元URL：** [Ollama Library](https://ollama.com/library), [Ollama Embedding Models](https://ollama.com/blog/embedding-models), 2024年6月更新

---

## 比較サマリー

### コスト効率性
- **最も安価：** Ollama（完全無料、ローカル実行）
- **商用最安：** OpenAI text-embedding-3-small ($0.02/1M)
- **無料利用：** Google Gemini API（制限付き無料枠）

### 性能面
- **最高性能：** OpenAI GPT-4.1、Gemini 2.5 Pro
- **コスパ最優秀：** Gemini 2.0 Flash、OpenAI GPT-4o-mini
- **ローカル最強：** Llama 4、DeepSeek-R1

### コンテキスト長
- **最長：** Gemini 1.5 Pro（2M トークン）
- **標準的：** OpenAI GPT-4.1（1M トークン）
- **ローカル：** Llama 3.1（128K-200K トークン）

### 埋め込み性能
- **最高次元：** OpenAI text-embedding-3-large（3,072次元）
- **バランス型：** Gemini embedding-exp（3,072次元）
- **ローカル最強：** mxbai-embed-large（OpenAI超えの性能）

---

## 注意事項

1. **価格情報：** 2024年6月時点の公開情報に基づく
2. **制限事項：** 各プラットフォームのレート制限、利用規約を確認必要
3. **更新頻度：** モデル仕様は頻繁に更新されるため、最新情報を確認推奨
4. **ローカル実行：** Ollamaはハードウェア要件（GPU、メモリ）に依存

**最終更新：** 2024年6月14日