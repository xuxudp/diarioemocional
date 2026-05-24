import os
import base64
import requests
from dotenv import load_dotenv


# Carrega as variaveis do arquivo .env
load_dotenv()


# Pega as credenciais do Spotify salvas no .env
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


# Valida se as credenciais foram encontradas
if not client_id or not client_secret:
    raise Exception("SPOTIFY_CLIENT_ID ou SPOTIFY_CLIENT_SECRET nao encontrados no arquivo .env")


# Junta Client ID e Client Secret no formato exigido pelo Spotify
credenciais = f"{client_id}:{client_secret}"


# Converte as credenciais para Base64
credenciais_bytes = credenciais.encode("utf-8")
credenciais_base64 = base64.b64encode(credenciais_bytes).decode("utf-8")


# URL usada para pedir o token de acesso
url_token = "https://accounts.spotify.com/api/token"


# Headers enviados no POST do token
headers_token = {
    "Authorization": f"Basic {credenciais_base64}",
    "Content-Type": "application/x-www-form-urlencoded"
}


# Corpo da requisicao POST
data_token = {
    "grant_type": "client_credentials"
}


# Faz o POST para pegar o token
resposta_token = requests.post(url_token, headers=headers_token, data=data_token)


# Mostra o status da requisicao do token
print("Status token:", resposta_token.status_code)


# Se o token nao for gerado, mostra o erro e para o programa
if resposta_token.status_code != 200:
    print("Erro ao obter token:")
    print(resposta_token.text)
    exit()


# Transforma a resposta do Spotify em JSON
dados_token = resposta_token.json()


# Pega o access_token retornado pelo Spotify
token = dados_token["access_token"]


# ID fixo de uma musica para teste
id_musica = "11dFghVXANMlKmJXsNCbNl"


# URL usada para buscar dados da musica
url_musica = f"https://api.spotify.com/v1/tracks/{id_musica}"


# Header do GET usando o token recebido
headers_musica = {
    "Authorization": f"Bearer {token}"
}


# Faz o GET para buscar os dados da musica
resposta_musica = requests.get(url_musica, headers=headers_musica)


# Mostra o status da requisicao da musica
print("Status musica:", resposta_musica.status_code)


# Se a musica nao for encontrada, mostra o erro e para o programa
if resposta_musica.status_code != 200:
    print("Erro ao buscar musica:")
    print(resposta_musica.text)
    exit()


# Transforma a resposta da musica em JSON
dados_musica = resposta_musica.json()


# Extrai somente os campos que interessam
nome_musica = dados_musica["name"]
nome_artista = dados_musica["artists"][0]["name"]
nome_album = dados_musica["album"]["name"]
popularidade = dados_musica["popularity"]
duracao_ms = dados_musica["duration_ms"]
link_spotify = dados_musica["external_urls"]["spotify"]


# Exibe os dados tratados no terminal
print("\nMusica encontrada:")
print("Nome da musica:", nome_musica)
print("Artista:", nome_artista)
print("Album:", nome_album)
print("Popularidade:", popularidade)
print("Duracao em ms:", duracao_ms)
print("Link Spotify:", link_spotify)