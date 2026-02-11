import openai
import os
from dotenv import load_dotenv

load_dotenv()

class AIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    def get_completion(self, prompt, system_prompt="You are a helpful assistant."):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"