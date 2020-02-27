from gtts import gTTS
from pygame import mixer
import tempfile
import time

def speak(sentence,language='zh-tw',loop=1):
	with tempfile.NamedTemporaryFile(delete=True) as tf:
		tts=gTTS(text=sentence, lang=language)
		tts.save('{}.mp3'.format(tf.name))
		mixer.init()
		mixer.music.load('{}.mp3'.format(tf.name))
		mixer.music.play(loop)
		time.sleep(1)