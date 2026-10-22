import streamlit as st
from agent import ask_agent

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================================================
# 2. CUSTOM CSS
# ==================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8fafc 55%,
            #eef2ff 100%
        );
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 12px;
        margin-bottom: 12px;
        background-color: rgba(255, 255, 255, 0.75);
    }

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# 3. HEADER - NATIVE STREAMLIT COMPONENTS
# ==================================================

st.title("🤖 AI Agent")

st.caption(
    "Your intelligent conversational assistant"
)

st.divider()

# ==================================================
# 4. INITIALIZE CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# 5. WELCOME MESSAGE
# ==================================================

if not st.session_state.messages:

    st.info(
        "👋 Welcome! Ask me anything. "
        "I can use our previous messages to understand context."
    )

    st.markdown("### Try asking")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("- What is Artificial Intelligence?")
        st.markdown("- Explain Python programming.")

    with col2:
        st.markdown("- What is Machine Learning?")
        st.markdown("- Explain database management.")

# ==================================================
# 6. DISPLAY PREVIOUS MESSAGES
# ==================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.markdown(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(message["content"])

# ==================================================
# 7. CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Type your message and press Enter...",
    max_chars=1000
)

# ==================================================
# 8. PROCESS USER INPUT
# ==================================================

if user_input is not None:

    user_input = user_input.strip()

    # ----------------------------------------------
    # INPUT VALIDATION
    # ----------------------------------------------

    if not user_input:

        st.warning(
            "Please enter a message before submitting."
        )

    elif len(user_input) < 3:

        st.warning(
            "Your message is too short. "
            "Please enter at least 3 characters."
        )

    else:

        # ------------------------------------------
        # SAVE USER MESSAGE
        # ------------------------------------------

        previous_conversation = (
            st.session_state.messages.copy()
        )

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # ------------------------------------------
        # DISPLAY USER MESSAGE
        # ------------------------------------------

        with st.chat_message("user"):

            st.markdown(user_input)

        # ------------------------------------------
        # CALL AI AGENT
        # ------------------------------------------

        with st.chat_message("assistant", avatar="🤖"):

            with st.spinner("AI Agent is thinking..."):

                try:

                    response = ask_agent(
                        user_input,
                        previous_conversation
                    )

                    # ------------------------------
                    # VALIDATE AI RESPONSE
                    # ------------------------------

                    if (
                        isinstance(response, str)
                        and response.strip()
                    ):

                        st.markdown(response)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })

                    else:

                        st.warning(
                            "The AI agent returned an empty response. "
                            "Please try again."
                        )

                        st.session_state.messages.pop()

                except Exception as error:

                    st.error(
                        "Unable to get a response from the AI agent."
                    )

                    st.info(
                        "Check your API key, internet connection, "
                        "and Gemini model configuration, then try again."
                    )

                    # Print technical details in terminal
                    print("AI Agent Error:", repr(error))

                    # Remove failed user message
                    st.session_state.messages.pop()

# ==================================================
# 9. CLEAR CONVERSATION
# ==================================================

st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

# ==================================================
# 10. FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        AI Agent · Built with Python and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)