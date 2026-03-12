from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json
from dotenv import load_dotenv

# Load environment variables from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

app = FastAPI(title="Rural TeleHealth AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SymptomRequest(BaseModel):
    text_content: str
    language: str = "en" # en, hi, pa

def get_llm_response(prompt: str):
    primary_provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    backup_provider = os.getenv("LLM_BACKUP_PROVIDER", "groq").lower()
    
    def call_provider(provider: str):
        if provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            # Find JSON in response text (Gemini sometimes adds backticks)
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            return json.loads(text[start:end])
            
        elif provider == "groq":
            from groq import Groq
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        raise ValueError(f"Unknown provider: {provider}")

    try:
        # Try Primary
        print(f"Calling primary provider: {primary_provider}")
        return call_provider(primary_provider)
    except Exception as e:
        print(f"Primary ({primary_provider}) failed: {e}. Trying backup: {backup_provider}")
        try:
            # Try Backup
            return call_provider(backup_provider)
        except Exception as backup_e:
            raise HTTPException(status_code=500, detail=f"All AI providers failed. Backup error: {backup_e}")

@app.get("/")
async def root():
    return {"message": "Welcome to TeleHealth AI Service"}

@app.post("/api/ai/symptom-check/")
async def symptom_check(request: SymptomRequest):
    system_prompt = f"""
    You are a medical assistant for a rural telehealth system in India.
    Analyze the following symptoms provided by the user in {request.language}.
    
    USER SYMPTOMS: "{request.text_content}"
    
    Instructions:
    1. Respond in the SAME language as the input (Hindi, Punjabi, or English).
    2. Provide a summary of potential issues.
    3. Categorize urgency: LOW, MEDIUM, HIGH.
    4. provide a "Doctor Specialty" recommendation (e.g., General Physician, Pediatrician).
    5. ALWAYS include a disclaimer: "This is NOT a formal diagnosis. Consult a doctor immediately."
    
    Output MUST be in valid JSON format:
    {{
      "analysis": "...",
      "urgency": "...",
      "specialty": "...",
      "disclaimer": "...",
      "language_used": "..."
    }}
    """
    
    try:
        result = get_llm_response(system_prompt)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/api/ai/voice-to-text/")
async def voice_to_text(request: Request):
    """
    Endpoint to receive audio files (Hindi/Punjabi) and return English text.
    Uses Groq's Whisper-large-v3 for high-speed transcription.
    """
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # In a real scenario, you'd handle the multipart file upload properly
    # This is a template for the transcription logic
    try:
        # Example of how to call transcription if it were a file:
        # transcription = client.audio.transcriptions.create(
        #     file=("symptoms.mp3", await request.body()),
        #     model="whisper-large-v3",
        #     language="hi" # Or pa
        # )
        # return {"text": transcription.text}
        return {"status": "ready", "message": "Voice endpoint is configured. Ready for multi-part file uploads."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
