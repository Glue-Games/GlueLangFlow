from serverLogic.settings import API_KEY, CHAT_THEME
from openai import OpenAI

client = OpenAI(api_key=API_KEY)

def get_chat_gpt_response(messages):
    if len(messages) <= 1:
        messages.insert(0, CHAT_THEME)

    chat = client.chat.completions.create(model="gpt-4-0125-preview", messages=messages)
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return messages

def get_chat_gpt_prompt(level_caption):
    messages = [{"role": "user", "content": level_caption}]
    messages.insert(0, CHAT_THEME)

    chat = client.chat.completions.create(model="gpt-4-0125-preview", messages=messages)
    reply = chat.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return reply

def main():
    messages = [CHAT_THEME]

    while True:
        message = input("User: ")
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = client.chat.completions.create(model="gpt-4-0125-preview", messages=messages)

        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()