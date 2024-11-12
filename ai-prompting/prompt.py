import os
import openai
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


def prompt_chatgpt(prompt: str, max_tokens: int = 100) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        # Extract and return the assistant's reply
        return response['choices'][0]['message']['content']

    except openai.error.RateLimitError:
        print("Rate limit exceeded. Waiting before retrying...")
        time.sleep(30)
        return prompt_chatgpt(prompt, max_tokens)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    response = prompt_chatgpt(user_prompt)
    print("ChatGPT Response:", response)
