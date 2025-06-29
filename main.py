import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import time
import json

#load api key to env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "context_data" not in st.session_state:
    st.session_state.context_data = ""
if "bot_id" not in st.session_state:
    st.session_state.bot_id = None
if "convo_id" not in st.session_state:
    st.session_state.convo_id = None
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "emails" not in st.session_state:
    st.session_state.emails = []
if "refresh" not in st.session_state:
    st.session_state.refresh = False

if st.session_state.refresh:
    st.session_state.refresh = False
    st.rerun()
# send email
def send_email(to: str, subject: str, body: str):
    print(f"Email to {to}: {subject}\n{body}")
    return {"status": "Email sent successfully"}

def handle_tool_call(tool_call):
    if tool_call.function.name == "send_email":
        args = json.loads(tool_call.function.arguments)
        result = send_email(args["to"], args["subject"], args["body"])
        return {"tool_call_id": tool_call.id, "output": json.dumps(result)}
    return None

def reset_email():
    st.session_state.emails.clear()
    st.session_state.chat_log.clear()
    st.session_state.refresh = True
    
# css for profile
st.markdown(
    """
    <style>
    .profile {
        position: absolute;
        top: 10px;
        right: 10px;
        color: #333333;
        font-family: sans-serif;
        font-size: 16px;
        padding: 5px 10px;
        background-color: #F0F0F0;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# main content
st.title("Context Restricted Chatbot")

st.header("Training input")
context_input = st.text_area(
    "Paste reference info (FAQs, product descriptions, etc.):",
    height=200,
    value=st.session_state.context_data
)

# save context
if st.button("Save Context"):
    if context_input.strip():
        try:
            st.session_state.context_data = context_input
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "send_email",
                        "description": "Send an email",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "to": {"type": "string"},
                                "subject": {"type": "string"},
                                "body": {"type": "string"}
                            },
                            "required": ["to", "subject", "body"]
                        }
                    }
                }
            ]
            assistant = client.beta.assistants.create(
                name="Trained Chatbot",
                instructions=(
                    f"You are a chatbot that answers questions strictly based on the following training content:\n\n"
                    f"{context_input}\n\n"
                    f"If a question is out of scope, respond with: "
                    f"\"I'm sorry, I can only answer questions based on the provided training content.\""
                ),
                model="gpt-4o",
                tools=tools
            )
            st.session_state.bot_id = assistant.id
            convo = client.beta.threads.create()
            st.session_state.convo_id = convo.id
            st.success("Bot trained successfully!")
        except Exception as e:
            st.error(f"Bot creation failed: {str(e)}")
    else:
        st.error("Training content is required.")

st.header("Ask the Bot")
if st.session_state.bot_id and st.session_state.convo_id:
    for msg in st.session_state.chat_log:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Your question:")
    if user_prompt:
        try:
            st.session_state.chat_log.append({"role": "user", "content": user_prompt})
            with st.chat_message("user"):
                st.write(user_prompt)

            client.beta.threads.messages.create(
                thread_id=st.session_state.convo_id,
                role="user",
                content=user_prompt
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state.convo_id,
                assistant_id=st.session_state.bot_id
            )

            while run.status not in ["completed", "requires_action"]:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.convo_id,
                    run_id=run.id
                )
                time.sleep(1)

            if run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                results = [handle_tool_call(tc) for tc in tool_calls if handle_tool_call(tc)]
                if results:
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=st.session_state.convo_id,
                        run_id=run.id,
                        tool_outputs=results
                    )
                    while run.status != "completed":
                        run = client.beta.threads.runs.retrieve(
                            thread_id=st.session_state.convo_id,
                            run_id=run.id
                        )
                        time.sleep(1)

            messages = client.beta.threads.messages.list(thread_id=st.session_state.convo_id)
            reply = messages.data[0].content[0].text.value
            st.session_state.chat_log.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)

        except Exception as e:
            st.error(f"Chat failed: {str(e)}")
else:
    st.warning("Train the bot first using reference data.")
    
# Register email
if not st.session_state.emails:
    st.header("Register Your Email")
    email = st.text_input("Your email address:")
    if st.button("Submit Email"):
        if email and "@" in email:
            st.session_state.emails.append(email)
            st.success("Email saved!")
            try:
                client.beta.threads.messages.create(
                    thread_id=st.session_state.convo_id,
                    role="user",
                    content=f"Send an email to {email} with subject 'Welcome' and body 'Thanks for signing up!'"
                )
                run = client.beta.threads.runs.create(
                    thread_id=st.session_state.convo_id,
                    assistant_id=st.session_state.bot_id
                )
                while run.status not in ["completed", "requires_action"]:
                    run = client.beta.threads.runs.retrieve(
                        thread_id=st.session_state.convo_id,
                        run_id=run.id
                    )
                    time.sleep(1)
                if run.status == "requires_action":
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    outputs = [handle_tool_call(tc) for tc in tool_calls if handle_tool_call(tc)]
                    if outputs:
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=st.session_state.convo_id,
                            run_id=run.id,
                            tool_outputs=outputs
                        )
            except Exception as e:
                st.error(f"Failed to send email: {str(e)}")
        else:
            st.error("Enter a valid email.")
# profile
st.sidebar.header("Profile")
if st.session_state.emails:
    st.sidebar.write(f"Registered Email: {st.session_state.emails[-1]}")
    if st.sidebar.button("Add another email", key="add_another_email", on_click=reset_email):
        pass  
else:
    st.sidebar.write("No email registered.")