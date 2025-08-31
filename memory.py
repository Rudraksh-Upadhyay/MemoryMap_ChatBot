
import json
import os
import requests

class TemporaryMemory:
    def __init__(self):
        self.conversation = []

    def add(self, user_input, bot_response):
        """Add a user-bot message pair to the conversation."""
        self.conversation.append({"role":"user", "content":user_input})
        self.conversation.append({"role":"assistant", "content":bot_response})

    def get_history(self):
        """return the conversation history"""
        return self.conversation

    def reset(self):
        """clears the memory"""
        self.conversation = []

class PermanentMemory:
    def __init__(self, filename = "memory.json"):
        self.filename = filename

    def save(self, temp_memory):
        """save the conversation from TemporaryMemory to JSON file"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(temp_memory.get_history(), f, indent=2)

    def load(self):
        """load the conversation from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


    def clear_file(self):
        """delete memory file"""
        if os.path.exists(self.filename):
            os.remove(self.filename)


EURON_API_KEY = os.getenv("EURON_API_KEY")

def get_euron_response(messages, model="gpt-5-mini-2025-08-07", temperature=0.7, max_tokens=1000):
    """
    calls the Euron API and returns the assistant's reply.
    messages = [{"role":"user", "content":"...."}, {"role":"assistant", "content":"...."}]

    """

    url = "https://api.euron.one/api/v1/euri/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURON_API_KEY}"
    }
    payload = {
        "messages": messages,
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]