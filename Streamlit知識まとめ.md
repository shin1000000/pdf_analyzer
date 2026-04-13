# Streamlit 知識まとめ

## 1. Streamlitとは

PythonだけでブラウザのUIが作れるフレームワーク。HTMLもCSSも不要。

```python
import streamlit as st

st.title("タイトル")
st.file_uploader("ファイルをアップロード")
st.button("実行")
st.dataframe(df)
st.download_button("ダウンロード", data=csv)
```

これだけでアップロード・ボタン・表・ダウンロードが揃ったUIになる。

---

## 2. ターミナルスクリプトとStreamlitアプリの違い

```
pdf_analyzer.py（ターミナル）
　→ PDFパスをコードに直書き
　→ print()で表示
　→ csvファイルに保存
　→ ターミナルで実行

app.py（Streamlit）
　→ アップロードUIで選択
　→ st.dataframe()で表示
　→ ダウンロードボタン
　→ ブラウザで操作
```

**ロジック（APIを呼ぶ処理）は同じ。UIだけが違う。**

---

## 3. ファイル構成（長期運用の理想形）

今の構成（学習段階）：
```
pdf_analyzer.py  ← ターミナル版
app.py           ← Streamlit版（ロジックがコピペ状態）
```

理想の構成（社内展開時）：
```
API_study/
  core/
    analyzer.py     ← ロジックだけ（API呼び出し）
  prompts/
    extraction.txt  ← system prompt
  app.py            ← StreamlitがanalyzerをUI化するだけ
  cli.py            ← ターミナル版がanalyzerを呼ぶだけ
```

**core/analyzer.pyを直せば両方に反映される。アプリが増えても管理が楽。**

---

## 4. 起動方法

```bash
# ローカルで起動
python -m streamlit run app.py

# ブラウザで開く
http://localhost:8501
```

---

## 5. APIキーの管理（ローカル vs クラウド）

```python
# ローカルは.env、Streamlit Cloudはsecretsから読む
api_key = st.secrets.get("ANTHROPIC_API_KEY") if "ANTHROPIC_API_KEY" in st.secrets \
          else os.environ.get("ANTHROPIC_API_KEY")
```

| 環境 | APIキーの管理方法 |
|---|---|
| ローカル | .envファイル |
| Streamlit Cloud | 管理画面のSecretsに設定 |
| Azure | サーバーの環境変数に設定 |

**.envファイルはどの環境でもGitHubに上げない。**

---

## 6. デプロイ先の選択肢

| | Streamlit Cloud | Azure App Service |
|---|---|---|
| 費用 | 無料〜（Publicリポジトリ限定） | 約2,000円/月〜 |
| 難易度 | 簡単（GitHubと連携するだけ） | 少し複雑 |
| リポジトリ | Publicのみ無料 | Privateでも可 |
| 社内利用 | コードが公開されるためNG | ✅ |
| Microsoft連携 | なし | OneDrive・SharePointと親和性高い |

**学習・検証：Streamlit Cloud（Public）**
**社内本番運用：Azure（Private）**

---

## 7. GitHubリポジトリの公開設定

| | Public | Private |
|---|---|---|
| 誰が見れる？ | 世界中 | 許可した人だけ |
| Streamlit Cloud無料枠 | ✅ | ❌（有料プラン必要） |
| 社内コードの管理 | NG | ✅ |

社内展開するなら**Privateリポジトリ + Azure**が現実的。

---

## 8. Azureの費用感

```
Azure App Service B1：約2,000円/月
Claude API費用    ：数千円/月（使い方次第）
─────────────────────────────────────
合計              ：月5,000円以内に収まる可能性が高い
```

### 費用確認の流れ

```
1. IT部門に確認
   「Microsoft 365の契約でAzure使えますか？」
   「Azureのテナントが子会社単位であるか？」

2. 使える → 追加契約不要、サーバー費用だけ
   使えない → 新規契約 or 親会社に相談
```

Microsoft 365を既に契約していればAzureアカウントがついてくる場合がある。親会社・子会社で管理が分かれているケースも多いのでIT部門への確認が最初のステップ。

---

## 9. 社内展開のロードマップ

```
1. ローカルで動作確認（今ここ）
　　↓
2. GitHubにコード管理（Private）
　　↓
3. Azureにデプロイ → 社内全員がブラウザからアクセス可能
　　↓
4. system promptのGUI化 → 現場担当者が自分で調整できる
```
