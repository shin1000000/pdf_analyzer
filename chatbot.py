import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

conversation_history = []

print("Claude チャットボット起動！（終了するには 'quit' または 'exit' と入力）")
print("-" * 50)

while True:
    user_input = input("\nあなた: ").strip()

    if user_input.lower() in ["quit", "exit", "終了"]:
        print("終了します。またね！")
        break

    if not user_input:
        continue

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system="あなたは関西弁で話すアシスタントです。必ず関西弁で返答してください。",
        messages=conversation_history
    )

    assistant_message = response.content[0].text

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    print(f"\nClaude: {assistant_message}")
