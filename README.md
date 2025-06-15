## 埋め込みプロバイダとモデルの指定

`--provider embedding` を使用する際は、以下のフラグで埋め込みサービスとモデルを指定できます:

- `--embed-provider <openai|gemini|ollama>`: 埋め込みプロバイダを指定します (デフォルト: openai)
- `--embed-model <EMBED_MODEL>`: 埋め込みモデル識別子を指定します (例: text-embedding-ada-002, models/embedding-gecko-001)

### 例

- OpenAI 埋め込みで分類:
  ```bash
  python tag_refiner.py \
    --provider embedding \
    --embed-provider openai \
    --embed-model text-embedding-ada-002 \
    --api-key $OPENAI_API_KEY \
    --input-dir PATH_TO_CLIPPINGS
  ```

- Gemini 埋め込みで分類:
  ```bash
  python tag_refiner.py \
    --provider embedding \
    --embed-provider gemini \
    --embed-model models/embedding-gecko-001 \
    --api-key $GOOGLE_API_KEY \
    --input-dir PATH_TO_CLIPPINGS
  ```

- Ollama 埋め込みで分類:
  ```bash
  python tag_refiner.py \
    --provider embedding \
    --embed-provider ollama \
    --embed-model my-embed-model \
    --input-dir PATH_TO_CLIPPINGS
  ```
# Obsidian Tag Refiner

Obsidian の Clippings/ フォルダ内 Markdown ノートを、LLM（OpenAI, Gemini, Ollama）のいずれかを使って自動分類し、YAML Frontmatter に `tags` プロパティを付与するスクリプトです。

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Tags Taxonomy](#tags-taxonomy)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)

## Features
- Clippings/ 以下のすべての `.md` ファイルを再帰的に走査
- 記事内容を LLM で解析し、事前定義された階層タグに分類
- YAML Frontmatter を自動更新して `tags` プロパティを付与
- OpenAI, Google Gemini, Ollama の切り替え対応
- Dry-run モードで実際の書き換えを確認可能

## Prerequisites
- Python 3.8 以上
- pip
- (推奨) virtualenv
- LLM プロバイダ用の API キーまたはローカルモデル
  - OpenAI: `OPENAI_API_KEY`
  - Gemini: `GOOGLE_API_KEY`
  - Ollama: `ollama` CLI とローカルにダウンロード済みモデル

## Installation
1. リポジトリまたはスクリプト配布フォルダをクローン/コピー
2. スクリプトディレクトリに移動:
   ```bash
   cd private_works/scripts/codex/tag_refiner
   ```
3. (任意) virtualenv の作成・有効化:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. 依存パッケージをインストール:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
### タグ定義 (tags.yml)
`tags.yml` にタグ階層を YAML 形式で定義します。例:
```yaml
research:
  - papers
  - bio_agri
dev:
  - agents
  - tools
  - tutorials
# …
```  
このファイルをカスタマイズすることで、分類先のタグを自由に編集できます。

### 環境変数
API キーは環境変数または `--api-key` 引数で指定します:
- `OPENAI_API_KEY` (OpenAI)
- `GOOGLE_API_KEY` (Gemini)

## Usage
基本コマンド:
```bash
python tag_refiner.py \
  --embed-provider <openai|gemini|ollama> \
  --embed-model <EMBED_MODEL> \
  --provider <openai|gemini|ollama|embedding> \
  --model <MODEL_NAME> \
  [--api-key <API_KEY>] \
  --input-dir <NOTES_DIR> \
  [--tags-file <TAGS_YAML>] \
  [--dry-run] [--dry-run-limit <NUM>]
```

- `--provider`: 使用するプロバイダ (openai, gemini, ollama, embedding; デフォルト: openai)
- `--model`: モデル識別子 (例: `gpt-4.1`, `gemini-2.5-flash-preview-05-20`, `llama4`)
- `--api-key`: API キー (OpenAI/Gemini 用)
- `--input-dir`: Markdown ノートのルートディレクトリ (必須)
- `--tags-file`: タグ定義ファイルのパス (デフォルト: `tags.yml`)
- `--dry-run`: Frontmatter を書き換えずに、更新内容をコンソール出力 (最初の `--dry-run-limit` 件のみ処理)
- `--dry-run-limit`: dry-run モード時に処理するファイル数 (デフォルト: 10)

## Examples
 - OpenAI (gpt-4.1) で Dry-run（最初のデフォルト10件）:
   ```bash
   python tag_refiner.py \
     --provider openai \
     --model gpt-4.1 \
    --api-key $OPENAI_API_KEY \
    --input-dir Clippings \
    --dry-run
  ```
- Dry-runで処理件数を5件に制限:
  ```bash
  python tag_refiner.py \
    --provider openai \
    --model gpt-4 \
    --api-key $OPENAI_API_KEY \
    --input-dir Clippings \
    --dry-run \
    --dry-run-limit 5
  ```
 - Gemini (Google) で本番実行:
   ```bash
   python tag_refiner.py \
     --provider gemini \
     --model gemini-2.5-flash-preview-05-20 \
    --api-key $GOOGLE_API_KEY \
    --input-dir Clippings
  ```
 - Ollama (ローカルモデル llama4):
   ```bash
   python tag_refiner.py --provider ollama --model llama4 --input-dir Clippings
   ```
 - 埋め込み（OpenAI Embeddings）で分類（上位3タグ取得）:
   ```bash
   python tag_refiner.py \
     --provider embedding \
     --model text-embedding-3-small \
     --api-key $OPENAI_API_KEY \
     --input-dir Clippings
   ```
 

## Tags Taxonomy
サンプルの `tags.yml`:
```yaml
# Sample tag taxonomy - customize for your vault
sample_category:
  - example_tag1
  - example_tag2
another_category:
  - tagA
  - tagB
misc:
  - uncategorized
```  
上記を参考に `tags.yml` を編集してタグ階層を定義してください。

## Troubleshooting
- 分類が意図しない場合は、`--dry-run` でノートの本文とタグ候補を確認し、`tags.yml` を調整してください。
- API レスポンスの JSON 解析エラーは、LLMの出力整形が原因です。`system_prompt` や `user_prompt` を調整するか、`temperature=0` を維持してください。
- Ollama 実行エラー: `ollama` CLI のパスやモデル名を確認。

## Contributing
- バグ報告・機能追加は Pull Request または Issue を立ててください。
- タグ階層の変更は `tags.yml` に直接反映できます。

## Generate Taxonomy

Obsidian ノート一覧から日本語のタグ階層を自動生成するスクリプトです。
生成結果はカテゴリ／サブカテゴリの階層マッピングのみを含み、元のノートタイトルは出力されません。
```bash
python generate_taxonomy.py \
  --provider <openai|gemini|ollama> \
  --model <MODEL_NAME> \
  --api-key <API_KEY> \
  --input-dir <NOTES_DIR> \
  [--depth <N>] \        # タクソノミー階層の最大深度 (デフォルト:3)
  [--use-embedding] \    # 埋め込み＋クラスタリングでタイトルを要約
  [--embed-provider <openai|gemini|ollama>] \
  [--embed-model <EMBED_MODEL>] \
  [--clusters <N>] \     # クラスタ数 (デフォルト:10)
  [--output <file>] \ # 保存先 (デフォルト: tags_YYMMDD.yml)
  [--dry-run]            # 標準出力のみ (ファイル未書き込み)
```
* `--depth`: タクソノミー階層の最大深度を指定
* `--use-embedding`: タイトルを埋め込みベースでクラスタリングし、代表タイトルに要約後に分類
* `--clusters`: クラスタリングによってまとめるグループ数（代表タイトル数）を指定 (デフォルト:10)。
  - この数だけ代表タイトルを抽出し、その少数のタイトルを基に LLM がタグ階層を生成します。

## Setup
Install dependencies:
```
pip install -r requirements.txt
```
Prepare or customize the tag taxonomy in `tags.yml` (default file provided next to the script).

## Usage
```
python tag_refiner.py \
    [--provider openai|gemini|ollama|embedding] \
    [--model MODEL_NAME] \
    [--api-key API_KEY] \
    --input-dir PATH_TO_CLIPPINGS \
    [--tags-file PATH_TO_TAGS_YAML] \
    [--dry-run]
```

- `--provider`: which provider to use: openai (completion), gemini, ollama, or embedding (default: openai)
- `--model`: model identifier (e.g. `gpt-4`, `chat-bison-001`, `llama2`)
- `--api-key`: API key for OpenAI or Google (overrides env vars)
- `--input-dir`: directory of Markdown notes (required)
- `--tags-file`: path to YAML file defining tags taxonomy (default: `tags.yml` next to script)
- `--dry-run`: show planned updates without writing files

## Examples
```
# OpenAI with gpt-4
python tag_refiner.py --provider openai --model gpt-4 --api-key $OPENAI_API_KEY --input-dir PATH_TO_CLIPPINGS

# Gemini (Google) with chat-bison-001, using default tags.yml
python tag_refiner.py \
    --provider gemini \
    --model chat-bison-001 \
    --api-key $GOOGLE_API_KEY \
    --input-dir PATH_TO_CLIPPINGS
    
# Using custom taxonomy file
python tag_refiner.py \
    --provider openai \
    --model gpt-4 \
    --api-key $OPENAI_API_KEY \
    --input-dir PATH_TO_CLIPPINGS \
    --tags-file /path/to/custom_tags.yml

 # Ollama local LLM (e.g., llama2)
 python tag_refiner.py --provider ollama --model llama2 --input-dir PATH_TO_CLIPPINGS
 # Embedding (OpenAI Embeddings)
 python tag_refiner.py --provider embedding \
   --model text-embedding-ada-002 \
   --api-key $OPENAI_API_KEY \
   --input-dir PATH_TO_CLIPPINGS
```