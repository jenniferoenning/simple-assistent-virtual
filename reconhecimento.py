import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from random import randint

def cria_audio(audio, mensagem):
	tts = gTTS(mensagem, lang="pt-br")
	tts.save(audio)
	playsound(audio)

cria_audio("welcome.mp3", "Escolha um número entre 1 a 10.")
recon = sr.Recognizer()

with sr.Microphone() as source:
	print("Diga algo")
	audio = recon.listen(source)


numero = recon.recognize_google(audio, language="pt-br")

resultado = randint(1,10)

 == resultado:
	cria_audio("venceu.mp3", "Parabéns. Você acertou o número. Tete jogar na mega sena!")
else:
	cria_audio("perdeu.mp3", "Infelizmente você errou. Tente novamente!")