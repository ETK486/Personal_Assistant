from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import FastAPI,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()
app=FastAPI()

with open("system.md",'r') as f:
    system_prompt=f.read().strip()

class Message(BaseModel):
    message:str

client=genai.Client()
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.post("/prompt")
async def get_prompt(prompt:Message):
    try:
        prompt=prompt.message
        response=await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )
        return response.text
    except Exception as e:
        return e.message

@app.get("/")
async def get_homepage():
    return FileResponse("static/Homepage.html")
