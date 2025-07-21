import google.generativeai as genai
import os
from typing import List, Tuple, Optional


def configure_gemini():
    """Configure Gemini API with your API key"""
    api_key = os.getenv("GOOGLE_API_KEY")  
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    genai.configure(api_key=api_key)

def get_gemini_response(messages: List[Tuple[str, str]], system_instruction: Optional[str] = None) -> str:
    """
    Get response from Gemini API
    
    Args:
        messages: List of (role, content) tuples where role is 'user' or 'model'
        system_instruction: Optional system instruction for the model
    
    Returns:
        str: The model's response
    """
    try:
        configure_gemini()
        
        
        model_name = "gemini-1.5-flash"  
        
        if system_instruction:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
        else:
            model = genai.GenerativeModel(model_name=model_name)
        
        
        chat_history = []
        current_message = None
        
        for role, content in messages:
            if role == "user":
                if current_message:
                    chat_history.append(current_message)
                current_message = {"role": "user", "parts": [content]}
            elif role == "model":
                if current_message:
                    chat_history.append(current_message)
                current_message = {"role": "model", "parts": [content]}
        
        
        if len(messages) > 1:
            
            chat = model.start_chat(history=chat_history[:-1])  
            if current_message and current_message["role"] == "user":
                response = chat.send_message(current_message["parts"][0])
            else:
                
                response = chat.send_message("")
        else:
            
            if current_message and current_message["role"] == "user":
                response = model.generate_content(current_message["parts"][0])
            else:
                response = model.generate_content("")
        
        return response.text
        
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"


def get_gemini_response_rest(messages: List[Tuple[str, str]], system_instruction: Optional[str] = None) -> str:
    """
    Alternative implementation using REST API directly
    """
    import requests
    import json
    
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        
        contents = []
        for role, content in messages:
            if role in ["user", "model"]:  
                contents.append({
                    "role": role,
                    "parts": [{"text": content}]
                })
        
        payload = {"contents": contents}
        
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
        
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Error: No response generated"
            
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"