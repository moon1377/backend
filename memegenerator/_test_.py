import requests

url = 'https://api.imgflip.com/get_memes'

# hacemos peticion
response = requests.get(url)

# convertimos la respuesta a JSON 
response_json = response.json()

print("Status:", response_json['success'])

# vemos primer meme
first_meme = response_json['data']['memes'][0]
print("----------------")
print("Nombre:", first_meme['name'])
print("URL Imagen:", first_meme['url'])