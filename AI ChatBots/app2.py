import os
import gradio as gr
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load the Hugging Face token from .env
load_dotenv()


HF_TOKEN = os.getenv("HF_TOKEN")


if not HF_TOKEN:
    raise ValueError("HF_TOKEN was not found in the .env file.")


# Create Hugging Face client
client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)


# AI model
MODEL = "Qwen/Qwen3.8-27B"




def chatbot(message, history):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, friendly AI assistant. "
                "Answer the user's questions clearly and accurately."
            )
        }
    ]


    # Add previous conversation
    if history:
        for item in history:
            if isinstance(item, dict):
                messages.append(item)


    # Add current user message
    messages.append({
        "role": "user",
        "content": message
    })


    try:
        response = client.chat_completion(
            messages=messages,
            model=MODEL,
            max_tokens=512,
            temperature=0.7
        )


        return response.choices[0].message.content


    except Exception as e:
        return f"Sorry, an error occurred: {str(e)}"




demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 AI Chatbot",
    description="Ask me anything!",
)


demo.launch()
