from django.shortcuts import render
from google import genai
import os

# vista principal para chatbot
def chat_view(request):
    response_text = None # ia
    user_prompt = None # user


    if request.method == 'POST': # verifica si fue enviado
        user_prompt = request.POST.get('prompt') # obtiene el texto
        
        api_key = os.environ.get("GEMINI_API_KEY") 

        if user_prompt and api_key: # si hay texto y api key
            try:
                client = genai.Client(api_key=api_key) # crea un cliente para conectarse usando la clave
                response = client.models.generate_content(
                    model="gemini-2.5-flash", # modelo que usamos
                    contents=user_prompt # texto quye debe procesar
                )
                response_text = response.text #obtiene respuesta de gemini
                
            except Exception as e: #si hay error
                response_text = f"Error al conectar con la IA: {e}"
        elif not api_key:
             response_text = "Error: No se encontró la API KEY configurada." #si no hay api

    #modifica el index
    return render(request, 'chatbot/index.html', {
        'response': response_text,
        'user_prompt': user_prompt
    })