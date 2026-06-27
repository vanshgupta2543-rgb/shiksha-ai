\# Shiksha AI — Voice-Enabled AI Teaching Assistant



A hands-free AI co-pilot for live classroom sessions in Haryana government schools.

Built for the Connecting Dreams Foundation Round 2 Technical Assignment.



\---



\## What it does



Shiksha AI helps teachers explain concepts and run quizzes using only their voice — no typing, no clicking mid-lesson. It speaks back in natural Hinglish and projects bilingual subtitles (English + Devanagari) on the smartboard in real time.



\*\*Feature 1 — Live Concept Simplification\*\*

Teacher speaks or types a topic. The AI explains it in conversational Hinglish with rolling bilingual subtitles and a spoken explanation via neural Hindi TTS.



\*\*Feature 2 — Voice-Triggered Quizzing\*\*

Teacher speaks a topic and selects question count. The AI generates a Hinglish MCQ quiz, reads questions aloud, accepts student answers by voice or text, and evaluates them instantly with feedback.



\---



\## Tech Stack



| Layer | Tool |

|---|---|

| UI \& Deployment | Streamlit + Streamlit Community Cloud |

| Speech-to-Text | faster-whisper (base model, CPU) |

| LLM | Groq API — Llama 3.3 70B Versatile |

| Text-to-Speech | edge-tts — Microsoft Neural hi-IN-SwaraNeural |

| Language | Python 3.13 |



\---



\## Prompt Design



Two system prompts live in `/prompts`:



\*\*`simplify.txt`\*\* — Instructs the LLM to generate a single fluid Hinglish explanation (not two separate languages), along with a sentence-level subtitle array containing English and Devanagari versions of each sentence. This powers the rolling bilingual subtitle display synced with TTS playback.



\*\*`quiz.txt`\*\* — Instructs the LLM to generate NCERT-aligned MCQ questions in Hinglish with one clearly correct answer and a brief Hinglish explanation for the correct option. Enables voice answer evaluation via a third prompt that checks student responses with cultural empathy ("Koi baat nahi! Dobara try karo").



Key prompt decisions:

\- Hinglish over pure Hindi or English — mirrors how teachers in Haryana actually speak

\- Relatable Indian examples — farms, cricket, chai, festivals over abstract analogies

\- JSON-only responses — strict output format prevents hallucinated structure and makes parsing reliable

\- Warm, encouraging tone — explicitly instructed to sound like a favourite teacher, not a textbook



\---



\## Localization



\- STT language hint set to `hi` in faster-whisper — handles Hinglish and code-switched speech

\- TTS uses `hi-IN-SwaraNeural` — Microsoft's neural Hindi voice that handles embedded English words naturally

\- Devanagari subtitles rendered via Google Fonts (Baloo 2) loaded in the Streamlit CSS layer

\- UI copy entirely in Hinglish — buttons, labels, and feedback messages mirror classroom language



\---



\## Run Locally



```bash

git clone https://github.com/vanshgupta2543-rgb/shiksha-ai.git

cd shiksha-ai

python -m venv venv

venv\\Scripts\\activate        # Windows

pip install -r requirements.txt

```



Create a `.env` file:

GROQ\_API\_KEY=your\_key\_here



Run:

```bash

streamlit run app.py

```



\---



\## Project Structure

shiksha-ai/



├── app.py              # Main Streamlit app



├── stt.py              # faster-whisper STT wrapper



├── llm.py              # Groq LLM calls + prompt loading



├── tts.py              # edge-tts neural Hindi TTS



├── prompts/



│   ├── simplify.txt    # Concept simplification system prompt



│   └── quiz.txt        # Quiz generation system prompt



├── requirements.txt



└── README.md



\---



\## Built by



Vansh — Technology Lead, Politics Personal

CDF Round 2 Technical Assignment

