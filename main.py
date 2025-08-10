import streamlit as st
import requests
import json
import time
import logging

# Set page configuration
st.set_page_config(
    page_title="🌱 Mindful Journal AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS styling with background image
st.markdown("""
<style>
    :root {
        --primary: #1a73e8;
        --secondary: #202124;
        --sidebar-bg: #1a1d23;
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #2d3436;
        --text-secondary: #5f6368;
    }

    .stApp {
        background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8)), url('https://images.unsplash.com/photo-1497864149936-d3163f0c0f4b');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: var(--text-primary);
    }

    .st-emotion-cache-6qob1r {
        background: var(--sidebar-bg) !important;
        border-right: 1px solid #2d3436;
    }

    .stChatMessage {
        background: var(--card-bg) !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        backdrop-filter: blur(2px);
    }

    [data-testid="stChatMessage"][aria-label="assistant"] {
        border-left: 4px solid var(--primary);
    }

    .stButton>button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 24px !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(26, 115, 232, 0.2);
    }

    .journal-card {
        background: var(--card-bg) !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        backdrop-filter: blur(3px);
    }

    h1, h2, h3 {
        color: var(--text-primary) !important;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }

    p, li {
        color: var(--text-secondary) !important;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Welcome to your Mindful Journal 🌸 Let's cultivate mental wellness together."
    }]

# Configure sidebar
with st.sidebar:
    st.title("⚙️ Journal Settings")
    with st.container():
        api_key = st.text_input("OpenRouter API Key", type="password")
        st.markdown("[Get API Key](https://openrouter.ai/keys)")
        
        with st.expander("📖 Quick Start"):
            st.markdown("""
            1. Set daily intention
            2. Choose analysis depth
            3. Explore features:
               - Mood tracking
               - Emotional patterns
               - Guided reflections
            """)
        
        model_name = st.selectbox(
            "🤖 Analysis Model",
            ("google/palm-2-chat-bison",),
            index=0
        )
        
        with st.expander("🧘 Wellness Settings"):
            current_mood = st.select_slider(
                "🌈 Current Mood",
                options=["😔 Stressed", "😐 Neutral", "🙂 Content", "😊 Positive", "😄 Joyful"]
            )
            analysis_depth = st.selectbox(
                "🔍 Reflection Depth",
                ["Brief Check-in", "Moderate Reflection", "Deep Analysis"]
            )
        
        if st.button("✨ New Session", use_container_width=True):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "New journal session started 🌱 Share your thoughts..."
            }]

# Main interface
st.title("📔 Mindful Journal AI")
st.caption("Your compassionate companion for emotional wellness and self-reflection")

# Feature cards
with st.container():
    cols = st.columns(4)
    features = [
        ("🌦️ Mood Tracking", "Visualize emotional patterns"),
        ("🧩 Stress Analysis", "Identify triggers"),
        ("💭 Guided Prompts", "Structured reflections"),
        ("📆 Progress Insights", "Growth over time")
    ]
    for col, (emoji, text) in zip(cols, features):
        col.markdown(
            f"""<div class='journal-card'>
                <h4>{emoji} {text}</h4>
            </div>""", 
            unsafe_allow_html=True
        )

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat interface
if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    if not api_key:
        with st.chat_message("assistant"):
            st.error("🔑 API key required for emotional insights")
            st.markdown("""
            <div style='background: rgba(255,255,255,0.9); padding: 15px; border-radius: 15px;'>
                <h4 style='color: var(--text-primary);'>Getting Started:</h4>
                <ol style='color: var(--text-secondary);'>
                    <li>Visit <a href="https://openrouter.ai/keys" style='color: var(--primary);'>OpenRouter</a></li>
                    <li>Create wellness account</li>
                    <li>Enter credentials above</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        st.stop()

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("🌱 Reflecting on your thoughts..."):
            time.sleep(0.5)
        
        try:
            # Add a dynamic session ID and timestamp to avoid cached identical responses
            dynamic_prompt = f"""
            You are a compassionate mental health ally. GUIDELINES:
            1. Respond with empathetic, non-judgmental support
            2. Structure reflections:
               - Emotional Validation
               - Pattern Recognition
               - Gentle Probing Questions
               - Coping Strategies
            3. Use nature-inspired emojis: 🌱🌸🌧️🌈
            4. Current Mood: {current_mood}
            5. Analysis Depth: {analysis_depth}
            6. Never make diagnoses
            7. Maintain therapeutic boundaries

            Session Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
            Session ID: {time.time_ns()}
            """

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://mindful-journal.streamlit.app",
                    "X-Title": "AI Mental Health Companion"
                },
                json={
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": dynamic_prompt}
                    ] + st.session_state.messages,  # Full history for better context
                    "temperature": 0.8,  # More variation
                    "response_format": {"type": "text"}
                },
                timeout=20
            )

            response.raise_for_status()
            data = response.json()
            raw_response = data['choices'][0]['message']['content']
            
            # Format response
            processed_response = raw_response.replace("**", "").replace("```", "")
            
            # Stream response word by word
            lines = processed_response.split('\n')
            for line in lines:
                words = line.split()
                for word in words:
                    full_response += word + " "
                    response_placeholder.markdown(full_response + "▌")
                    time.sleep(0.03)
                full_response += "\n"
                response_placeholder.markdown(full_response + "▌")
            
            # Final formatting
            full_response = full_response.replace(
                "Reflection:", "<span style='color: var(--primary)'>Reflection:</span>"
            ).replace(
                "Coping Strategy:", "<span style='color: #7A918D'>Coping Strategy:</span>"
            )
            
            response_placeholder.markdown(full_response, unsafe_allow_html=True)
            
        except Exception as e:
            logging.error(f"Reflection Error: {str(e)}")
            response_placeholder.error("🍃 Gentle Reminder: It's okay to take a breath and try again")

    st.session_state.messages.append({"role": "assistant", "content": full_response})

