import os
import gradio as gr
from google import genai


# ==========================================
# GEMINI API KEY
# ==========================================

api_key = os.environ.get("vip")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Go to Render > Environment and add "
        "GEMINI_API_KEY with your Gemini API key."
    )


# ==========================================
# GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)


# ==========================================
# QUESTION GENERATOR
# ==========================================

def generate_questions(topic, difficulty, number_of_questions):

    if not topic or not topic.strip():
        return "Please enter a topic."

    prompt = f"""
You are an interactive question generator.

Generate exactly {int(number_of_questions)} questions.

Topic: {topic}
Difficulty Level: {difficulty}

Instructions:
- Generate exactly {int(number_of_questions)} questions.
- Number the questions from 1 to {int(number_of_questions)}.
- Do not provide answers.
- Do not provide explanations.
- Make every question relevant to the topic.
- Match the selected difficulty level.

Difficulty guidelines:

Easy:
Basic concepts, definitions, and simple understanding.

Medium:
Application, comparison, and moderate reasoning.

Hard:
Analysis, problem solving, and advanced reasoning.

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
# GRADIO APPLICATION
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
# START SERVER
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 7860))

    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
