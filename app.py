from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Swaroop Talakwar"
        self.linkedin = ""
        self.resume = ""
        
        reader = PdfReader("me/Profile.pdf")
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        
        resume_reader = PdfReader("me/Swaroop_resume (1).pdf")
        for page in resume_reader.pages:
            text = page.extract_text()
            if text:
                self.resume += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "\
    "You are also given a resume of {self.name} which you can use to answer questions.Never provide my personal phone number to the user"

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n## Resume:\n{self.resume}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1800px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        padding: 1.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.95;
        font-weight: 300;
    }
    .chat-container {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1rem;
    }
    .chatbot {
        min-height: 600px !important;
        height: 600px !important;
    }
    button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }
    """
    
    # Create a custom theme
    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
    ).set(
        body_background_fill="*neutral_50",
        button_primary_background_fill="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        button_primary_background_fill_hover="linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%)",
        button_primary_text_color="white",
        border_color_accent="*primary_300",
        shadow_spread="6px",
        block_border_width="2px",
        block_border_width_dark="2px",
    )
    
    # Create the interface with custom components
    with gr.Blocks(theme=theme, css=custom_css, title=f"Chat with {me.name}") as demo:
        gr.HTML(f"""
        <div class="main-header">
            <h1>👋 Chat with {me.name}</h1>
            <p>Ask me anything about my experience, skills, and background!</p>
        </div>
        """)
        
        chatbot = gr.Chatbot(
            label="Conversation",
            height=600,
            show_label=True,
            bubble_full_width=False,
            type="messages",
            container=True,
            show_copy_button=True,
            scale=1,
            value=[],
        )
        
        msg = gr.Textbox(
            label="Your Message",
            placeholder="Type your message here and press Enter to send...",
            show_label=True,
            lines=1,
            container=True,
        )
        
        with gr.Row():
            submit_btn = gr.Button("Send 💬", variant="primary", scale=1)
            clear_btn = gr.Button("Clear 🗑️", variant="secondary", scale=1)
        
        def respond(message, chat_history):
            if not message.strip():
                return chat_history, ""
            bot_message = me.chat(message, chat_history)
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": bot_message})
            return chat_history, ""
        
        # Enable Enter key to send message (Shift+Enter for new line)
        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        submit_btn.click(respond, [msg, chatbot], [chatbot, msg])
        clear_btn.click(lambda: ([], ""), None, [chatbot, msg])
    

#     demo.launch(
#     server_name="localhost",  # or just omit this line entirely
#     server_port=7860,
#     share=True,               # gives you a temporary *.gradio.live link
# )


    