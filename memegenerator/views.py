from django.shortcuts import render

# Create your views here.

import requests

def index(request):
    # peticion a la api
    url = 'https://api.imgflip.com/get_memes'
    response = requests.get(url)
    data = response.json()
    
    # lista de memes
    memes = data['data']['memes']
    
    return render(request, 'memegenerator/index.html', {'memes': memes})