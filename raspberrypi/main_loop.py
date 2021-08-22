
from typing import Sequence
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
from datetime import datetime
from software.back_end_logic.ai_logic.face_recognition_testing import start_testing
from software.back_end_logic.db_logic.db_utils import db
from raspberrypi.reading_patients_serial import get_patients
from raspberrypi.sound.bot_voice import voice
from time import perf_counter
from raspberrypi.serial_comm import communicator

def get_current_time():
	hour, minute = datetime.now().hour, datetime.now().minute
	current_time = TimeOfDay(hour, minute)
	return current_time
def get_time_difference(t_initial: TimeOfDay, t_final: TimeOfDay) -> float:

	"""
	:param t_initial: Initial time as a TimeOfday object
	:param t_final: Final time as a TimeOfDay object
	:return: The time difference in minutes as a float
	"""

	hour_difference = t_final.hour - t_initial.hour
	minute_difference = t_final.minute - t_initial.minute

	return abs(hour_difference * 60 + minute_difference)

def has_med_time_come_for_patient(patient: Patient, leeway_minutes = 30):
	"""
	:param patient: Patient to check for
	:param leeway_minutes: How much leeway you're gonna give when looking at patients' medication time
	:return: a list of medications to take
	"""
	current_time = get_current_time()

	medications_to_take = []
	for med in patient.medications:
		for i in range(len(patient.medications[med])):
			potential_time = patient.medications[med][i]
			time_passed = get_time_difference(current_time, potential_time)
			# print(current_time.hour, current_time.minute, " - ", potential_time.hour, potential_time.minute, time_passed, patient.medications_last_taken[med][i])
			if time_passed < leeway_minutes and patient.can_patient_take_medication(med, i): #this checks if enought time has passed
				medications_to_take.append(med)

	return medications_to_take

def turn_on(patient_list: Sequence[Patient] = None, COM_PORT_NAME = "", language = "en", threshold = 80, greeting_time_limit_seconds = 10):
	"""

	:param patient_list (optional, if not specified the program will read from serial): List of patient objects that are registered as patients
	:param language: Language of the voice
	:param threshold: How many minutes before or after their actual time each person can take their medications
	:param greeting_time_limit_seconds: How many seconds the person waits for each person before greeting them again (to avoid the bot constantly spamming hello)
	:return: null
	"""
	if patient_list is None:
		patient_list = get_patients()

	for p in patient_list:
		print(p.name, )
		for k in p.medications:
			for j in p.medications[k]:
				print(j.hour, j.minute)
		print()
	ARDUINO_COMMUNICATOR = communicator(COM_PORT_NAME)
	last_greeted_time_for_patients = {}
	for p in patient_list:
		last_greeted_time_for_patients[p.name] = -100000000


	medication_indexes = db.get_sorted_meds()

	for name in start_testing(threshold):
		# constantly loops through people that have been recognized by the ai
		# yes, this is a for loop, but it is infinite because the start_testing function goes on forever and only yields a face when it recognizes someone
		print("person recognized ")
		for p in patient_list: #checking to see if person is the current patient we are looking at
			if name.lower() in p.name.lower() and perf_counter() - last_greeted_time_for_patients[p.name] > greeting_time_limit_seconds:
				#the ai has recognized someone who is registered as a patient.

				ARDUINO_COMMUNICATOR.send_to_arduino("d")
				voice.say("Hello " + p.name + "!", language)
				meds_to_take = has_med_time_come_for_patient(p) #if the person has not taken medications today, this returns a list of meds

				#start a thread that sends stuff to ardunio in the background:
				ARDUINO_COMMUNICATOR.send_all_meds_to_arduino_with_thread(meds_to_take)

				if len(meds_to_take) == 0:
					voice.say("You do not need to take any medications at the moment.", language)

				else:
					strMed = ""
					for i in range(len(meds_to_take) - 1):
						strMed += meds_to_take[i] + ", "

					if len(meds_to_take) > 1:
						strMed += "and "

					strMed += meds_to_take[-1]

					voice.say("At the moment, you will be taking", language)
					voice.say(strMed, language)




				last_greeted_time_for_patients[p.name] = perf_counter()

				break


if __name__ == '__main__':


	#temporarily simulating data for testing: (I don't want to actually initiate serial communication every time I'm testing)
	# patients = {'Emre Cenk': {'Asprin': [(0, 0), (12, 0)], 'Talcid': [(17, 0), (17, 0)], 'Xanax': [(0, 0)], 'Beta': [(0, 0)]}, 'Alternative Cenk': {'Ibuprofen': [(0, 0), (12, 0)]}}
	# patients = db.convert_to_patient_objects(patients)
	# turn_on(patient_list = patients, language = "en")
	turn_on()
