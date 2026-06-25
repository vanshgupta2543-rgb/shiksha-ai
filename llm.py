import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def load_prompt(filename: str) -> str:
    base = os.path.dirname(__file__)
    with open(os.path.join(base, "prompts", filename), "r", encoding="utf-8") as f:
        return f.read()

def simplify_concept(topic: str) -> dict:
    system = load_prompt("simplify.txt")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Explain this topic: {topic}"}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"explanation": raw, "key_points": [], "hindi_word": "", "emoji_visual": "📚"}

def generate_quiz(topic: str, num_questions: int = 3) -> dict:
    system = load_prompt("quiz.txt")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": f"Generate {num_questions} questions on: {topic}"}
        ],
        temperature=0.7,
        max_tokens=800
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"questions": []}

def evaluate_answer(question: str, correct: str, student_answer: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful teacher. Evaluate if the student's answer is correct. Respond ONLY in JSON: {\"correct\": true/false, \"feedback\": \"brief encouraging feedback in Hinglish\"}"},
            {"role": "user", "content": f"Question: {question}\nCorrect answer: {correct}\nStudent said: {student_answer}"}
        ],
        temperature=0.3,
        max_tokens=200
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"correct": False, "feedback": "Dobara try karo!"}