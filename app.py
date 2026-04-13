import os
import base64
import io
import pandas as pd
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ローカルは.env、Streamlit Cloudはsecretsから読む
api_key = st.secrets.get("ANTHROPIC_API_KEY") if hasattr(st, "secrets") and "ANTHROPIC_API_KEY" in st.secrets else os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

system_prompt = """PDFの空室一覧表から、以下の4項目のみを抽出してください。

抽出項目：
- 物件名
- フロア（階）
- 面積（坪）
- 賃料単価

ルール：
- 出力はCSV形式（1行目はヘッダー）
- 成約済みも含めて全物件を抽出
- 賃料が「相談」の場合はそのまま「相談」と記載
- 余計な説明文は不要、CSVのみ出力"""

st.title("PDF解析ツール")
st.write("PDFをアップロードすると、物件情報を自動で抽出します。")

uploaded_file = st.file_uploader("PDFをアップロード", type="pdf")

if uploaded_file is not None:
    if st.button("解析実行"):
        with st.spinner("Claude APIで解析中..."):
            pdf_data = base64.standard_b64encode(uploaded_file.read()).decode("utf-8")

            response = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": "このPDFから物件名・フロア・面積・賃料を抽出してCSV形式で出力してください。"
                            }
                        ],
                    }
                ],
            )

            result = response.content[0].text

        st.success("解析完了！")

        df = pd.read_csv(io.StringIO(result))
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
        st.download_button(
            label="CSVダウンロード",
            data=csv,
            file_name="output.csv",
            mime="text/csv",
        )
