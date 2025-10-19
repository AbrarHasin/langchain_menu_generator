import streamlit as st
import sys
from pathlib import Path
import uuid

# Add the current directory to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_helper import generate_resturant_name_n_items, chat_with_memory

# Page configuration
st.set_page_config(page_title="Restaurant AI Assistant", page_icon="🍽️", layout="wide")

# Initialize session state for thread_id (maintains conversation across reruns)
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for mode selection
st.sidebar.title("🍽️ Restaurant AI Assistant")
mode = st.sidebar.radio(
    "Choose Mode:",
    ["Restaurant Name Generator (Legacy)", "Chat with Memory (New)"],
    index=1
)

# Add conversation controls
st.sidebar.markdown("---")
if st.sidebar.button("🔄 New Conversation"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.chat_history = []
    st.rerun()

st.sidebar.markdown(f"**Conversation ID:** `{st.session_state.thread_id[:8]}...`")

# Main content area
if mode == "Restaurant Name Generator (Legacy)":
    st.title("🏪 Restaurant Name Generator")
    st.markdown("*Simple restaurant name generation based on country*")

    country = st.text_input("Enter a Country name for Restaurant Name:")

    if country:
        with st.spinner("Generating restaurant name..."):
            response = generate_resturant_name_n_items(country)
            st.header(response['resturant_name'].strip())

else:  # Chat with Memory mode
    st.title("💬 Chat with Memory (LangGraph 2025)")
    st.markdown("*Have a conversation with persistent memory across messages*")

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything about restaurants, cuisines, or food..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response with memory
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_prompt = "You are a knowledgeable restaurant and culinary expert. Help users with restaurant ideas, menu suggestions, cuisine information, and food-related questions. Be friendly, creative, and informative."

                response = chat_with_memory(
                    user_message=prompt,
                    thread_id=st.session_state.thread_id,
                    system_prompt=system_prompt
                )

                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# Footer with instructions
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 How to Use:

**Legacy Mode:**
- Enter a country name
- Get a restaurant name suggestion

**Chat with Memory Mode:**
- Type messages in the chat
- AI remembers the conversation
- Start new conversation anytime

### 🔑 Key Features:
- ✅ Persistent conversation memory
- ✅ Multiple conversation threads
- ✅ Context-aware responses
- ✅ Powered by LangGraph 2025
""")