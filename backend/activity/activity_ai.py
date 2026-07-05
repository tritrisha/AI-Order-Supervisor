from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://aicredits.in/v1"   
)


def generate_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content


def summarize(messages):
    summary_prompt = [
        {
            "role": "system",
            "content": "Summarize the conversation in 2 short sentences."
        },
        {
            "role": "user",
            "content": str(messages)
        }
    ]

    return generate_ai_response(summary_prompt)