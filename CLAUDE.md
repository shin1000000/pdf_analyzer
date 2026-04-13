# プロジェクト引き継ぎ：Claude API チャットボット構築

## 背景・目的

データ入力業務のオペレーション改善を目的として、LLM（Claude API）を活用したツールを構築する。
現状はPDF・HP・WebのデータをExcelや社内システムに手動で打ち込んでいる作業を自動化・効率化したい。

### 担当者のスキル感
- Pythonは経験あり（現在はClaude CodeやCodexに丸投げしてスクリプト作成）
- Power Automateの構築経験あり（複雑な処理はPythonの方が使いやすいと判断済み）
- VSCode + Claude Code環境構築済み（Windows）
- OneDrive経由でのファイル管理に慣れている

### 使用ツール（社内）
- Slack
- SharePoint / OneDrive
- Microsoft Office（Excel等）
- ChatGPT Business
- Confluence

---

## やりたいこと

### フェーズ1：チャットボット（ターミナルベース）
- Claude APIを使ったシンプルな対話型チャットボット
- まずターミナル上で動作するものを作る

### フェーズ2：PDF・画像解析
- PDFや画像ファイルを投げ込んで内容を解析
- 指定したルール（MDファイル等）に従って表形式（Excel）に出力する
- 想定フロー：PDFをインプット → Claude APIで解析 → Excelに出力

### フェーズ3：GUI化ロードマップ
1. **ターミナル**（現在地）
2. **Streamlit**：ブラウザベースのUIを追加、社内ツールとして使いやすくする
3. **Slack**：Slackbot化して既存の業務フローに組み込む

---

## 技術スタック

- 言語：Python
- LLM：Claude API（Anthropic）
- GUIフレームワーク（予定）：Streamlit
- ファイル操作：openpyxl（Excel出力）、PyPDF2またはpdfplumber（PDF読み取り）

---

## 環境・セットアップ状況

- [x] Git for Windows インストール済み
- [x] Claude Code インストール済み（VSCode拡張含む）
- [x] Anthropic Console アカウント作成済み
- [x] APIキー発行済み（キーはローカルに保存済み）
- [ ] Pythonインストール確認
- [ ] anthropicライブラリインストール
- [ ] .envファイルによるAPIキー管理設定

---

## APIキー管理ルール（重要）

- APIキーは`.env`ファイルに記載し、コードには直接書かない
- `.env`ファイルは`.gitignore`に追加してGitHubに上げない
- コード内では環境変数から読み込む

```python
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
```

---

## 比較検証するLLM

API学習にあたって、以下のLLMを実際に使って精度・機能の差分を比較検証する。

| LLM | API | 管理コンソール |
|---|---|---|
| Claude | Anthropic API | platform.claude.com |
| ChatGPT | OpenAI API | platform.openai.com |
| Gemini | Google AI API | aistudio.google.com |

### 比較検証の観点
- PDF読み取り精度
- 表形式出力の安定性
- 日本語の精度
- 指示への忠実さ
- レスポンス速度
- コスト（トークン単価）

### 方針
- まずClaude APIで基本的な実装を覚える
- 同じスクリプトでLLMを差し替えて比較する
- 業務用途（PDF解析・データ入力自動化）に最適なLLMを選定する

---

## 最初にやること

1. Pythonがインストールされているか確認：`python --version`
2. anthropicライブラリをインストール：`pip install anthropic`
3. `.env`ファイルを作成してAPIキーを設定
4. シンプルなターミナルチャットボットを作成・動作確認
