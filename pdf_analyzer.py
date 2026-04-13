import os
import base64
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PDF_PATH = "CBRE_PM_TOKYO_Property_Listing.pdf"

print(f"PDFを読み込み中: {PDF_PATH}")
with open(PDF_PATH, "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

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

print("Claude APIに送信中...")
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
print("\n===== 抽出結果 =====")
print(result)

with open("output.csv", "w", encoding="utf-8-sig") as f:
    f.write(result)

print("\noutput.csv に保存しました！")
