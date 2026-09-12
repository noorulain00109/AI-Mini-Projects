import gradio as gr

def chatbot(message, history):
    message = message.lower()

    if "hello" in message or "hi" in message:
        return "Hello! 👋 How can I help you today?"

    elif "how are you" in message:
        return "I'm doing great! 😊 How can I help you?"

    elif "your name" in message:
        return "I'm an AI chatbot created for your project."

    elif "machine learning" in message:
        return "Machine learning is a branch of AI that allows computers to learn patterns from data and make predictions or decisions."

    elif "thank" in message:
        return "You're welcome! 😊"

    elif "bye" in message:
        return "Goodbye! Have a great day! 👋"

    else:
        return "I'm sorry, I don't understand that yet. Please try asking another question."


demo = gr.ChatInterface(
    fn=chatbot,
    title="🤖 AI Chatbot",
    description="Ask me a question!",
)

demo.launch()
