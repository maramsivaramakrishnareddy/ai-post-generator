from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests, json, os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remote API URL (Groq)
url = "https://api.groq.com/openai/v1/chat/completions"

@app.post("/generatePost")
async def generatePost(request: Request):
    try:
        body = await request.json()
        topic = body.get('topic')
        if not topic:
            return {"error": "Please provide 'topic' in JSON body."}

        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": topic}
            ],
            "model": "llama-3.3-70b-versatile"
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"  # Load from env
  # Load from env
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return {
                "error": "Remote API error",
                "status_code": response.status_code,
                "body": response.text
            }

        data = response.json()
        res = data['choices'][0]['message']['content']
        return {"post": res}

    except Exception as e:
        return {"error": "Server exception", "details": str(e)}
