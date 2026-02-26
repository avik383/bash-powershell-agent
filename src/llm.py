import requests
import json
from bash import Bash
from config import ROOT_DIR as root

class LLMChat:
    
    def __init__(self, model: str, api_url: str, system_prompt: str = None):
        self.model = model
        self.api_url = api_url
        self.messages = []
        self.bash = Bash(cwd=root)
        if system_prompt:
            self.add_message("system", system_prompt)

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
    
    def query(self, message: str, tools: List[dict]):
        url = f"{self.api_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        self.add_message("user", message)
        payload = {
            "model": self.model,
            "messages": self.messages,
            "tools": tools,
            "tool_calls": "auto",
            "temperature": 0.7,
            "stream": False
        }

        response = requests.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
            data = response.json()

            if not response.ok or "object" not in data or data["object"] != "chat.completion":
                raise Exception(f"API Error: {data}")
            
            reply = data["choices"][0]["message"]
            self.add_message(reply["role"], reply.get("content", ""))
            return reply
        except Exception as e:
            pass
