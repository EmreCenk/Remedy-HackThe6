#This program caches TTS sound files in this directory for faster access, you can delete files to free up space but running this progam will take longer since it will recreate sound files.

import pyglet
import os
from time import sleep



class voice():
	
	@staticmethod
	def say(text: str, lg: str):

		os.listdir()

		fln = text + " " + lg + ".wav"

		if fln not in os.listdir():
			from gtts import gTTS
			import translators as ts

			maintext = ts.google(text, from_language='auto', to_language=lg)
			tts = gTTS(maintext, lang=lg)

			tts.save(fln)

		play = pyglet.media.load(fln, streaming=False)
		play.play()
		sleep(play.duration)



if __name__ == "__main__":
	voice.say("my name is bob", "en")

	voice.say("my name is bob", "en")
	voice.say("my name is bob", "tr")
