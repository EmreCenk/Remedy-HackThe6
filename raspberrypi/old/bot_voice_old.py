
import pyttsx3 as pyt
import translators as ts


class voice():


	def __init__(self, male_voice = False):

		self.engine = pyt.init()
		self.engine.setProperty("rate", 125) # the "rate" property specifies the words per minute


		#setting the voice:
		voices = self.engine.getProperty('voices')       #getting details of current voice
		self.engine.setProperty('voice', voices[male_voice].id)

        
	def say(self, what_to_say: str):
		"""Says something out loud using the self.engine property"""
		
		self.engine.say(what_to_say)
		
		self.engine.runAndWait()



example_voice = voice(male_voice = True)
example_voice.say("my name is bob")
