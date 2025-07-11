# Tag Refiner Setup Guide

## 設定手順

### 1. API キーの設定
`.env.example`ファイルを`.env`にコピーして、使用するプロバイダーのAPIキーを設定：

```bash
# .env.exampleファイルを.envにコピー
cp .env.example .env
```

その後、`.env`ファイルを編集して実際のAPIキーを設定：

#### OpenAI を使用する場合（推奨）
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```
- https://platform.openai.com/api-keys で取得
- デフォルトモデル: `o4-mini`（コスト効率が良い）

#### Google Gemini を使用する場合
```
GOOGLE_API_KEY=your-google-api-key-here
```
- https://makersuite.google.com/app/apikey で取得
- デフォルトモデル: `gemini-2.5-flash-preview-05-20`

#### Ollama を使用する場合（ローカル実行）
```
OLLAMA_HOST=http://localhost:11434
```
- APIキー不要
- 事前にOllamaサーバーを起動し、モデルをダウンロードしておく必要がある
- デフォルトモデル: `llama4`

### 2. 実行オプション
現在の起動スクリプトはOpenAI `o4-mini`を使用するように設定されています。
別のプロバイダーを使用する場合は、起動スクリプトを編集：

```bash
# Gemini を使用する場合
python tag_refiner.py --provider gemini --model gemini-2.5-flash-preview-05-20 --input-dir "..."

# Ollama を使用する場合
python tag_refiner.py --provider ollama --model llama4 --input-dir "..."

# Embedding分類を使用する場合
python tag_refiner.py --provider embedding --embed-provider openai --embed-model text-embedding-3-small --input-dir "..."
```

### 3. Obsidian Shell Commands Plugin設定
1. Obsidian の Community Plugins で "Shell Commands" をインストール・有効化
2. Settings > Shell Commands で新しいコマンドを追加：
   - Command: `tag_refiner_startup.bat` の絶対パス
   - Working directory: このプロジェクトのディレクトリ
   - Trigger: "Obsidian starts" にチェック

### 4. 実行確認
- Obsidian を再起動すると自動的にタグ付与処理が開始される
- 処理状況は `tag_processing_startup_YYYYMMDD_HHMMSS.log` ファイルで確認可能

## 利用可能なプロバイダーとモデル

### OpenAI
- **o4-mini**: 最新で最もコスト効率が良い（推奨）
- **gpt-4o**: 高精度だが高コスト
- **gpt-3.5-turbo**: 安価だが精度は中程度

### Google Gemini
- **gemini-2.5-flash-preview-05-20**: 最新の高速モデル
- **gemini-1.5-pro**: 高精度モデル

### Ollama（ローカル実行）
- **llama4**: 最新のLlamaモデル
- **mxbai-embed-large**: 埋め込みベース分類用

## ファイル説明
- `tag_refiner_startup.bat`: Windows用起動スクリプト
- `tag_refiner_startup.sh`: Linux/WSL用起動スクリプト  
- `.env`: API設定ファイル（gitignore済み）
- `tags.yml`: タグ分類体系定義
- `generate_taxonomy.py`: タグ体系自動生成スクリプト
- `embedding_classifier.py`: 埋め込みベース分類モジュール

## トラブルシューティング
- **API エラー**: `.env`ファイルのAPIキーが正しく設定されているか確認
- **モデルエラー**: 指定したモデルが利用可能か確認
- **Ollama エラー**: Ollamaサーバーが起動し、モデルがダウンロードされているか確認