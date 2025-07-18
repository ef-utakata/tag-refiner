# Obsidian Shell Commands 設定ガイド

Obsidian Shell Commands plugin を使用して、Obsidian 起動時に自動的にタグ付けを実行する設定方法を説明します。

## 前提条件

- Obsidian がインストールされている
- Shell Commands plugin がインストールされている
- `tag_refiner_startup_fixed.bat` が正常に動作している

## 設定手順

### 1. Shell Commands プラグインの設定

1. Obsidian の設定 → Community plugins → Shell Commands を開く

2. 新しいコマンドを追加:
   - **Shell command**: `C:\Users\endor\Documents\private\private_works\scripts\projects\tag_refiner\tag_refiner_startup_fixed.bat`
   - **Alias**: `Tag Refiner Auto`

### 2. 実行設定

1. **Shell**: `cmd.exe` を選択
2. **Working directory**: `C:\Users\endor\Documents\private\private_works\scripts\projects\tag_refiner`
3. **Timeout**: 300秒（5分）
4. **Background execution**: チェックを入れる（推奨）

### 3. イベント設定

1. **Events** タブで `Obsidian starts` にチェック
2. **Output channel**: `Notification` または `Ignore` を選択
   - `Notification`: 実行結果をObsidianに通知
   - `Ignore`: バックグラウンドで静かに実行

### 4. 詳細設定（オプション）

- **Confirmation**: 実行確認をスキップする場合はチェックを外す
- **Error handling**: エラー時の動作を設定
- **Output handling**: 出力の表示方法を設定

## 実行確認

1. Obsidianを再起動
2. 以下のファイルが生成されることを確認:
   ```
   tag_processing_startup_[日付]_[時刻].log
   ```

## ログの確認方法

### ログファイルの場所
```
C:\Users\endor\Documents\private\private_works\scripts\projects\tag_refiner\
```

### ログファイル名の形式
```
tag_processing_startup_[DDMMYYYY]_[HHMM].log
```

例: `tag_processing_startup_18072025_0901.log`

### ログの内容
- 実行設定の確認
- 処理されたファイル数
- スキップされたファイル（既にタグ付け済み）
- エラーメッセージ（もしあれば）

## トラブルシューティング

### 実行されない場合
1. バッチファイルのパスが正しいか確認
2. WSLが正常に起動するか確認
3. .envファイルにAPIキーが設定されているか確認

### エラーが発生する場合
1. ログファイルの内容を確認
2. 手動でバッチファイルを実行してエラーを特定
3. Conda環境が正しく設定されているか確認

### パフォーマンスの最適化
- 大量のファイルがある場合は、バックグラウンド実行を推奨
- タイムアウト時間を必要に応じて調整
- 既にタグ付けされたファイルは自動的にスキップされる

## セキュリティ考慮事項

- APIキーは.envファイルに安全に保存される
- バッチファイルは読み取り専用として設定することを推奨
- ログファイルには機密情報は含まれない

## 関連ファイル

- `tag_refiner_startup_fixed.bat`: メインの実行スクリプト
- `.env`: API設定ファイル
- `tags.yml`: タグ分類体系定義
- `README.md`: 全体的な使用方法