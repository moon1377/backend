from django.shortcuts import render
from google import genai
import os

def chat_view(request):
    response_text = None
    user_prompt = None

    if request.method == 'POST':
        user_prompt = request.POST.get('prompt')
        
        api_key = os.environ.get("GEMINI_API_KEY") 

        if user_prompt and api_key:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt
                )
                response_text = response.text
            except Exception as e:
                response_text = f"Error al conectar con la IA: {e}"
        elif not api_key:
             response_text = "Error: No se encontró la API KEY configurada."

    return render(request, 'chatbot/index.html', {
        'response': response_text,
        'user_prompt': user_prompt
    })