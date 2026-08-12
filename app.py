# Paste the app.py code I provided above here
import os
import gradio as gr
from google import genai


# ==========================================
# GET GEMINI API KEY
# ==========================================

try:
    # Google Colab
    from google.colab import userdata
    api_key = userdata.get("vip")

except ImportError:
    # Render
    api_key = os.environ.get("GEMINI_API_KEY")


# ==========================================
# CHECK API KEY
# ==========================================

if not api_key:
    raise ValueError(
        "Gemini API key not found. "
        "In Colab, create a secret named 'vip'. "
        "In Render, create an environment variable named 'GEMINI_API_KEY'."
    )


# ==========================================
# INITIALIZE GEMINI
# ==========================================

client = genai.Client(api_key=api_key)


# ==========================================
# QUESTION GENERATOR FUNCTION
# ==========================================

def generate_questions(topic, difficulty, number_of_questions):

    if not topic or not topic.strip():
        return "Please enter a topic."

    prompt = f"""
You are an interactive question generator.

Generate exactly {number_of_questions} questions.

Topic: {topic}
Difficulty Level: {difficulty}

Rules:
1. Generate exactly {number_of_questions} questions.
2. Number each question clearly from 1 to {number_of_questions}.
3. Do not provide answers.
4. Do not provide explanations.
5. Keep every question relevant to the topic.
6. Match the selected difficulty level.

Difficulty guidelines:

Easy:
- Basic definitions
- Simple concepts
- Basic understanding

Medium:
- Application
- Comparison
- Moderate reasoning

Hard:
- Analysis
- Problem solving
- Advanced reasoning

Return only the numbered questions.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "No questions were generated."

    except Exception as e:
        return f"Error generating questions: {str(e)}"


# ==========================================
# GRADIO INTERFACE
# ==========================================

demo = gr.Interface(
    fn=generate_questions,

    inputs=[
        gr.Textbox(
            label="Topic",
            placeholder="Example: Artificial Intelligence",
            lines=1
        ),

        gr.Dropdown(
            choices=["Easy", "Medium", "Hard"],
            value="Easy",
            label="Difficulty Level"
        ),

        gr.Slider(
            minimum=1,
            maximum=10,
            value=5,
            step=1,
            label="Number of Questions"
        )
    ],

    outputs=gr.Textbox(
        label="Generated Questions",
        lines=15
    ),

    title="Interactive Question Generator",

    description=(
        "Enter a topic, select a difficulty level, "
        "and choose the number of questions."
    ),

    submit_btn="Generate Questions",
    clear_btn="Clear",
    flagging_mode="never"
)


# ==========================================
# LAUNCH GRADIO
# ==========================================

# Google Colab
# share=True automatically finds an available port.

demo.launch(share=True)
