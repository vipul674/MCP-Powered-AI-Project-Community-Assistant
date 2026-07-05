from streamlit.runtime import uploaded_file_manager
from httpx._transports.default import ResponseStream
from streamlit import chat_message
import streamlit as st
import httpx
import json
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Community Assistant",
page_icon="🤖", layout="wide")
st.title("🤖 MCP-Powered AI Assistant")

st.markdown("""
    <style>
        /* Add a subtle gradient to the main background */
        .stApp {
        background: linear-gradient(to bottom right, #0e1117, #1a1c24);
        }

        /* Darken and style the sidebar */
        [data-testid="stSidebar] {
        background-color: #12141a;
        border-right: 1px solid #2b2b36;
        }

        /* Make headers pop with a brand color */
        h1, h2, h2 {
            color: #4da6ff !important;
            font-family: 'Inter', sans-serif;
            }

        /* Style the chat input box */
        .stChatInput {
            border-radius: 15px !important;
            border: 1px solid #4da6ff !important;    
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("Welcome to your intelligent Community Assisstant! Ask me to search Github, query your uploaded PDFs, or search the live web.")

with st.sidebar:
    st.header("📄 Knowledge Base")
    uploaded_file = st.file_uploader("Upload a PDF or TXT", type=["pdf", "txt", "md"])

    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Uploading and parsing..."):
                
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                res = httpx.post(f"{BACKEND_URL}/api/files/upload", files=files, timeout=30.0)

                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Success! Document split into {data['chunks']} chunks. ")
                else:
                    st.error(f"Upload failed: {res.text}")

if "messages" not in st.session_state:
    st.session_state.messages = []

def render_messages(msg_content):
    if "[ISSUE_PREVIEW]" in msg_content:
        try:
            parts = msg_content.split("[ISSUE_PREVIEW]")
            if parts[0].strip():
                st.markdown(parts[0].strip())
            
            json_str = parts[1].strip()
            data = json.loads(json_str)

            with st.container(border=True):
                st.subheader("📝 Issue Preview")
                st.markdown(f"**Repository:** `{data.get('repo', '')}`")
                st.markdown(f"**Title:** {data.get('title', '')}")
                st.markdown(f"**Labels:** {','.join(data.get('labels', []))}")
                st.markdown("**Body:**")
                st.info(data.get('body', ''))

                if st.button("Confirm & Create Issue", key=f"btn_{hash(msg_content)}"):
                    st.session_state.trigger_confirm = json_str
                    st.rerun()
        except Exception as e:
            st.markdown(msg_content)
    
    else:
        st.markdown(msg_content)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_messages(msg["content"])

# 1. Check if the user clicked the Confirm button, otherwise show chat input
prompt = None
is_hidden = False

if "trigger_confirm" in st.session_state and st.session_state.trigger_confirm:
    prompt = f"/confirm_issue {st.session_state.trigger_confirm}"
    st.session_state.trigger_confirm = None
    is_hidden = True
else:
    user_input = st.chat_input("Ask me about the Github repository...")
    if user_input:
        prompt = user_input

# 2. Process the prompt
if prompt:
    # Only display the user's message if it's not our hidden system command
    if not is_hidden:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
    else:
        with st.chat_message("user"):
            st.markdown("_Confirmed issue creation._")
        st.session_state.messages.append({"role": "user", "content": "_Confirmed issue creation._"})

    with st.chat_message("assistant"):
        try:
            def stream_generator():
                with httpx.stream(
                    "POST",
                    f"{BACKEND_URL}/api/chat_stream",
                    json={"message": prompt},
                    timeout=None
                ) as r:
                    r.raise_for_status()
                    for chunk in r.iter_text():
                        if chunk:
                            yield chunk
                            
            reply_text = st.write_stream(stream_generator)
            
        except Exception as e:
            reply_text = f"Error communicating with backend: {e}"
            st.error(reply_text)

    # Save the response to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply_text})
    
    # If the response contained a preview, quickly refresh to hide the raw text and show the UI!
    if "[ISSUE_PREVIEW]" in reply_text:
        st.rerun()
