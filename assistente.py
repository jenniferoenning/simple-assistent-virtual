from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
import sys
from datetime import datetime
import webbrowser
from bs4 import BeautifulSoup
from requests import get
import requests
import json
import tkinter as tk
import time
from translate import Translator
import translate

def cria_audio(audio, mensagem):
	tts = gTTS(mensagem, lang="pt-br")
	tts.save(audio)
	playsound(audio)
	os.remove(audio)

cria_audio("audios/welcome.mp3", "Olá sou o Jaruis, você precisa de ajuda?")

def monitora_audio():
	recon = sr.Recognizer()
	with sr.Microphone() as source:
		print("Escutando...")
		recon.pause_threshold = 0.5
		audio = recon.listen(source)

	try:
		print("Reconhecendo...")
		mensagem = recon.recognize_google(audio, language="pt-br")
		mensagem = mensagem.lower()
		executa_comandos(mensagem)

	except Exception as e:
		print(e)
		cria_audio("audios/welcome.mp3", "Pode repetir, por favor?...")
		executa_comandos(mensagem)

		return "Nada"

	return mensagem

def executa_comandos(mensagem):
	if 'fechar assistente' in mensagem or 'fechar programa' in mensagem:
		sys.exit()
	elif 'horas' in mensagem:
		hora = datetime.now().strftime("%H:%M")
		frase = f"Agora são{hora}"
		cria_audio("audios/mensagem.mp3", frase)
	elif 'desligar computador' and 'uma hora' in mensagem:
		os.system("shutdown -s -t 3600")
	elif 'desligar computador' and 'meia hora' in mensagem:
		os.system("shutdown -s -t 1800")
	elif 'cancelar desligamento' in mensagem:
		os.system("shutdown -a")
	elif 'toca' and 'phonk' in mensagem:
		playlists('phonk')
	elif 'toca' and 'corrida' in mensagem:
		playlists('corrida')
	elif 'toca' and 'meme' in mensagem:
		playlists('meme')
	elif 'toca' and 'lofi' in mensagem:
		playlists('lofi')
	elif 'toca' and 'festa' in mensagem:
		playlists('festa')
	elif 'notícias' in mensagem:
		ultimas_noticias()
	elif 'cotãção' and 'dólar' in mensagem:
		cotacao_moeda('Dólar')
	elif 'cotãção' and 'real' in mensagem:
		cotacao_moeda('Real')
	elif 'abrir' and 'sublime' in mensagem:
		abrir_programa('sublime')
	elif 'abrir' and 'google' in mensagem:
		abrir_programa('google')
	elif 'tempo' in mensagem or 'temperatura' in mensagem:
		previsao_tempo()
	elif 'pesquisar' in mensagem or 'google' in mensagem:
		pesquisa_google()
	elif 'lembrete' in mensagem:
		criar_stick()
	elif 'traduzir' and 'inglês' in mensagem:
		translate('Inglês')
	elif 'traduzir' and 'português' in mensagem:
		translate('Português')

def translate(traducao):
	if traducao == 'Inglês':
		s = Translator(from_lang="pt-br", to_lang='english')
		cria_audio("audios/mensagem.mp3", "Fale o que você precisa traduzir para o Inglês.")
		mensagem = monitora_audio()
		res = s.translate(mensagem)
		cria_audio("audios/mensagem.mp3", "Sua tradução de " + mensagem + " é " + res)
	elif traducao == 'Português':
		s = Translator(from_lang="english", to_lang='pt-br')
		cria_audio("audios/mensagem.mp3", "Fale o que você precisa traduzir para o Inglês.")
		mensagem = monitora_audio()
		res = s.translate(mensagem)
		cria_audio("audios/mensagem.mp3", "Sua tradução de " + mensagem + " é " + res)

def criar_stick():
	current_time = time.strftime("%H:%M")
	cria_audio("audios/welcome.mp3", "Bem vindo ao lembrete")
	time.sleep(2)
	cria_audio("audios/welcome.mp3", "Escreva o que precisa no lembrete")
	anotacao = monitora_audio()
	note = ("*%s") % anotacao
	time.sleep(1)
	root = tk.Tk()
	root.title("Noty")
	root.geometry("300x300")
	tk.Label(root, text=current_time).pack()
	tk.Label(root, text=note).pack()
	root.mainloop()

def pesquisa_google():
	cria_audio("audios/welcome.mp3", "Fale a pesquisa desejada no google.")
	pesquisa = monitora_audio()
	webbrowser.open('https://www.google.com/search?q=' + pesquisa)

def previsao_tempo():
    api_key = "API-KEY-OPENWEATHER" #generate your own api key from open weather
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    cria_audio("audios/welcome.mp3", "Fale a cidade desejada.")
    city_name = monitora_audio()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("Em " + city_name + " a temperatura é de " +
             str(int(current_temperature - 273.15)) + " graus celcius " + ", humidade de " 
             + str(current_humidiy) + " % "
             " e " + str(weather_description))
        print(r)
        cria_audio("audios/welcome.mp3", r)
    else:
        cria_audio("audios/welcome.mp3", "Não encontramos a cidade desejada..")

def cotacao_moeda(moeda):
	if moeda == "Dólar":
		requisicao = get('https://economia.awesomeapi.com.br/all/USD-BRL')
		cotacao = requisicao.json()
		nome = cotacao['USD']['name']
		data = cotacao['USD']['create_date']
		valor = cotacao['USD']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio("audios/mensagem.mp3",mensagem)
	elif moeda == "Real":
		requisicao = get('https://economia.awesomeapi.com.br/all/BRL-USD')
		cotacao = requisicao.json()
		nome = cotacao['BRL']['name']
		data = cotacao['BRL']['create_date']
		valor = cotacao['BRL']['bid']
		mensagem = f'Cotação do {nome} em {data} é {valor} reais'
		cria_audio("audios/mensagem.mp3",mensagem)

def ultimas_noticias():
	site = get("https://news.google.com/news/rss?ned=pt-br&gl=BR&h1=pt")
	noticias = BeautifulSoup(site.text, 'html.parser')
	for item in noticias.findAll('item')[:2]:
		mensagem = item.title.text
		print(mensagem)
		cria_audio("audios/mensagem.mp3", mensagem)

def playlists(musica):
	if musica == 'phonk':
		webbrowser.open('https://open.spotify.com/track/7jVH8CXr0MSpGheHOjN4NA?si=c219099b0a7c4e2f')
	elif musica == 'corrida':
		webbrowser.open('https://open.spotify.com/track/1OMvtjYhjtItuTzrp7NV99?si=f6a3c89a67a0404b')
	elif musica == 'lofi' or musica == 'lo-fi':
		webbrowser.open('https://open.spotify.com/track/1OMvtjYhjtItuTzrp7NV99?si=f6a3c89a67a0404b')
	elif musica == 'festa':
		webbrowser.open('https://open.spotify.com/track/0O6u0VJ46W86TxN9wgyqDj?si=ab041298fdff46c0')
	elif musica == 'meme':
		webbrowser.open('https://www.youtube.com/watch?v=_caMQpiwiaU')

def abrir_programa(programa):
	if programa == 'sublime':
		os.startfile("C:\Program Files\Sublime Text\sublime_text.exe")
	elif programa == 'google':
		os.startfile("C:\Program Files\Google\Chrome\Application\chrome.exe")

def main():
	while True:
		monitora_audio()

main()