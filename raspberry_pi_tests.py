

from raspberrypi.main_loop import turn_on
from software.back_end_logic.ai_logic.training_faces import train_model
if __name__ == '__main__':
	# patients = {'Emre Cenk': {'Asprin': [(0, 10), (12, 0)], 'Talcid': [(17, 0), (17, 0)], 'Xanax': [(0, 0)], 'Beta': [(0, 0)]}, 'Alternative Cenk': {'Ibuprofen': [(0, 0), (12, 0)]}}
	# from raspberrypi.main_loop import turn_on
	turn_on()


	# patients = convert_to_patient_objects(patients)
	#
	# print(has_med_time_come_for_patient(patients[0], leeway_minutes = 60))
	# print(has_med_time_come_for_patient(patients[0], leeway_minutes = 60))
	# train_model()
	# turn_on(patients, 60)

