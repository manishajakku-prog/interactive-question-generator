import os
import gradio as gr
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("Gemini API connected successfully!")

def generate_questions(topic, difficulty, number_of_questions):
    prompt = f"""
You are an interactive question generator.
Topic: {topic}
Difficulty: {difficulty}
Number of questions: {number_of_questions}

Generate exactly {number_of_questions} questions.
Number each question clearly.
Do not provide answers.
Make the questions relevant to the topic and appropriate
for the selected difficulty level.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()


demo = gr.Interface(
    fn=generate_questions,
    inputs=[
        gr.Textbox(label="Topic"),
        gr.Dropdown(
            choices=["easy", "medium", "hard"],
            label="Difficulty"
        ),
        gr.Slider(
            minimum=1,
            maximum=10,
            step=1,
            value=5,
            label="Number of Questions"
        )
    ],
    outputs=gr.Textbox(label="Generated Questions"),
    title="Interactive Question Generator"
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)
