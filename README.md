# Obsidian Tag Refiner

Obsidian の Clippings/ フォルダ内 Markdown ノートを、LLM（OpenAI, Gemini, Ollama）を使って自動分類し、YAML Frontmatter に `tags` プロパティを付与するスクリプトです。

## 主な機能

- **自動タグ分類**: ノート内容をLLMで解析し、事前定義されたタグ階層に自動分類
- **チェックボックス機能**: `tag_revision_needed` プロパティでタグ修正が必要なファイルをマーク
- **複数プロバイダー対応**: OpenAI、Gemini、Ollama、埋め込みベース分類をサポート
- **Obsidian起動時実行**: Shell Commands pluginで自動実行可能
- **バックグラウンド実行**: 大量ファイルの処理でもタイムアウトしない
- **00_indexディレクトリ除外**: インデックスファイルはタグ付与対象外

## セットアップ

詳細な設定手順は [SETUP.md](SETUP.md) を参照してください。

### 簡単セットアップ

1. APIキーの設定:
   ```bash
   cp .env.example .env
   # .envファイルを編集してAPIキーを設定
   ```

2. Obsidian Shell Commands plugin設定:
   - `tag_refiner_startup.bat` を起動時実行に設定

## 使用方法

### 基本コマンド
```bash
python tag_refiner.py \
  --provider <openai|gemini|ollama|embedding> \
  --model <MODEL_NAME> \
  --input-dir <NOTES_DIR> \
  [--dry-run]
```

### 主なオプション
- `--provider`: 使用するプロバイダ (openai, gemini, ollama, embedding)
- `--model`: モデル識別子 (o4-mini, gemini-2.5-flash-preview-05-20, llama4)
- `--input-dir`: Markdownノートのディレクトリ
- `--dry-run`: 実際の更新をせずに処理内容を確認

## 利用可能なプロバイダー

### OpenAI（推奨）
- **o4-mini**: 最新で最もコスト効率が良い
- **gpt-4o**: 高精度だが高コスト
- **text-embedding-3-small**: 埋め込みベース分類用

### Google Gemini
- **gemini-2.5-flash-preview-05-20**: 最新の高速モデル
- **gemini-1.5-pro**: 高精度モデル

### Ollama（ローカル実行）
- **llama4**: 最新のLlamaモデル
- **mxbai-embed-large**: 埋め込みベース分類用

## 埋め込みベース分類

`--provider embedding` を使用する際のオプション:

- `--embed-provider <openai|gemini|ollama>`: 埋め込みプロバイダを指定
- `--embed-model <MODEL>`: 埋め込みモデル識別子を指定

### 例

```bash
# OpenAI 埋め込みで分類
python tag_refiner.py \
  --provider embedding \
  --embed-provider openai \
  --embed-model text-embedding-3-small \
  --input-dir PATH_TO_CLIPPINGS

# Gemini 埋め込みで分類
python tag_refiner.py \
  --provider embedding \
  --embed-provider gemini \
  --embed-model gemini-embedding-exp-03-07 \
  --input-dir PATH_TO_CLIPPINGS

# Ollama 埋め込みで分類
python tag_refiner.py \
  --provider embedding \
  --embed-provider ollama \
  --embed-model mxbai-embed-large \
  --input-dir PATH_TO_CLIPPINGS
```

## 関連ツール

### タグ分類体系の自動生成 (generate_taxonomy.py)
Obsidian ノート一覧から日本語のタグ階層を自動生成:
```bash
python generate_taxonomy.py \
  --provider openai \
  --model o4-mini \
  --input-dir <NOTES_DIR> \
  [--depth 3] \
  [--output tags_YYMMDD.yml]
```

### インデックスノートの生成 (generate_index.py)
分類済みノートからObsidian Dataview対応のインデックスノートを生成:
```bash
python generate_index.py \
  --tags-file tags.yml \
  --input-dir <NOTES_DIR> \
  [--output Index.md]
```

## ファイル構成

- `tag_refiner.py`: メインスクリプト
- `embedding_classifier.py`: 埋め込みベース分類モジュール
- `generate_taxonomy.py`: タグ分類体系自動生成
- `generate_index.py`: インデックスノート生成
- `tags.yml`: タグ分類体系定義
- `SETUP.md`: 詳細セットアップガイド
- `.env.example`: API設定テンプレート
- `tag_refiner_startup.bat/.sh`: 起動スクリプト

## 実行例

### 基本実行（OpenAI）
```bash
python tag_refiner.py \
  --provider openai \
  --model o4-mini \
  --input-dir "/path/to/Clippings"
```

### Dry-run実行
```bash
python tag_refiner.py \
  --provider openai \
  --model o4-mini \
  --input-dir "/path/to/Clippings" \
  --dry-run \
  --dry-run-limit 5
```

### Gemini実行
```bash
python tag_refiner.py \
  --provider gemini \
  --model gemini-2.5-flash-preview-05-20 \
  --input-dir "/path/to/Clippings"
```

### Ollama実行
```bash
python tag_refiner.py \
  --provider ollama \
  --model llama4 \
  --input-dir "/path/to/Clippings"
```

## トラブルシューティング

- **API エラー**: `.env`ファイルのAPIキーが正しく設定されているか確認
- **モデルエラー**: 指定したモデルが利用可能か確認
- **Ollama エラー**: Ollamaサーバーが起動し、モデルがダウンロードされているか確認
- **分類精度**: `--dry-run`で結果を確認後、`tags.yml`のタグ定義を調整

## セキュリティ

- APIキーを含む`.env`ファイルはgitignoreに含まれており、リポジトリに含まれません
- 設定は`.env.example`をコピーして行ってください

## 依存関係

```bash
pip install -r requirements.txt
```

主要な依存関係:
- `openai`: OpenAI API
- `google-generativeai`: Google Gemini API
- `PyYAML`: YAML処理
- `scikit-learn`: 埋め込み分類（オプション）
- `numpy`: 数値計算（オプション）