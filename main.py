import streamlit as st
from models.llm_openai import llm_instance as openai_llm_instance
from models.llm_ollama import llm_instance as ollama_llm_instance  
from models.llm_anthropic import llm_instance as anthropic_llm_instance

# Page configuration
st.set_page_config(
    page_title="AI Multi-LLM Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px;
        animation: gradient 3s ease infinite;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9C27B0;
    }
    .thinking-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    .thinking-icon {
        font-size: 3rem;
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.4; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    .sidebar-header {
        color: #FF6B6B;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'thinking' not in st.session_state:
    st.session_state.thinking = False
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

def _build_llm(model_provider: str, model: str, temperature: float, timeout: int):
    if model_provider == "Anthropic":  
        return anthropic_llm_instance(model, temperature, timeout)
    elif model_provider == "OpenAI":
        return openai_llm_instance(model, temperature, timeout)
    elif model_provider == "Ollama":
        return ollama_llm_instance(model, temperature, timeout)
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

# Main title
st.markdown('<h1 class="main-title">🤖 AI Multi-LLM Chatbot 🌟</h1>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    
    # Login/Logout section
    st.markdown("### 👤 User Authentication")
    if not st.session_state.logged_in:
        username_input = st.text_input("Username", key="username_input")
        if st.button("🔓 Login", use_container_width=True):
            if username_input:
                st.session_state.logged_in = True
                st.session_state.username = username_input
                st.success(f"Welcome, {username_input}!")
                st.rerun()
            else:
                st.error("Please enter a username")
    else:
        st.success(f"👋 Logged in as: **{st.session_state.username}**")
        if st.button("🔒 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    
    # LLM Selection
    st.markdown("### 🤖 Select LLM Provider")
    llm_provider = st.selectbox(
        "Choose Provider:",
        ["OpenAI", "Anthropic", "Ollama"],
        key="llm_provider"
    )
    
    # Model Selection based on provider
    st.markdown("### 🎯 Select Model")
    model_options = {
        "OpenAI": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "Anthropic": ["Claude Opus 4.5", "Claude Haiku 4.x", "Claude Sonnet 4 and 4.5"],
        "Ollama": ["gemma:2b", "tinyllama:latest"]
    }
    
    selected_model = st.selectbox(
        "Choose Model:",
        model_options[llm_provider],
        key="selected_model"
    )
    
    # Temperature slider
    st.markdown("### 🌡️ Temperature")
    temperature = st.slider(
        "Creativity Level:",
        min_value=0.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        key="temperature"
    )
    
    # Timeout
    timeout = st.number_input("⏱️ Timeout (seconds)", min_value=10, max_value=300, value=60, step=10)
    
    st.divider()
    
    # Clear history button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Main chat area
# Display chat history
st.markdown("### 💬 Chat History")

# Show username if logged in
if st.session_state.logged_in:
    st.caption(f"💬 Chatting as: **{st.session_state.username}**")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 Assistant ({message.get('provider', 'AI')}):</strong><br>
                {message["content"]}
            </div>
        """, unsafe_allow_html=True)

# Thinking indicator
if st.session_state.thinking:
    st.markdown("""
        <div class="thinking-container">
            <div class="thinking-icon">🤔 Thinking...</div>
        </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Store current message for processing
    st.session_state.current_message = user_input
    
    # Show thinking indicator
    st.session_state.thinking = True
    st.rerun()

# Process LLM response
if st.session_state.thinking:
    try:
        # Build LLM instance
        llm = _build_llm(llm_provider, selected_model, temperature, timeout)
        
        # Get response
        result = llm.invoke(st.session_state.current_message)
        
        # Add assistant message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result.content,
            "provider": f"{llm_provider} - {selected_model}"
        })
        
        st.session_state.thinking = False
        st.rerun()
        
    except Exception as e:
        st.session_state.thinking = False
        st.error(f"❌ Error: {str(e)}")
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Error: {str(e)}",
            "provider": llm_provider
        })
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>Made with ❤️ using Streamlit | Multi-LLM Chatbot</div>",
    unsafe_allow_html=True
)
