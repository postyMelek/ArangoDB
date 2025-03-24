from langchain.llms.base import LLM
from typing import ClassVar,Optional, List
import google.generativeai as genai
import os

# Konfigurasi API KEY dari environment
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
genai.configure(api_key="AIzaSyBFwLYLneQD_QXGatzNybb2FHhua4GDjvk")

class GeminiLLM(LLM):
    # model_name = "gemini-1.5-pro-latest"  # Bisa juga "gemini-1.5-pro"
    model_name: ClassVar[str] = "gemini-1.5-pro-latest"  # Atau gemini-1.5-pro-latest
    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        return response.text
