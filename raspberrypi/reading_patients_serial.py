


import serial
import serial.tools.list_ports
from typing import List, Tuple
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
from software.back_end_logic.db_logic.db_utils import db

def read_patient(com_index = 0, create_local_db = False) -> dict:
	com_ports = serial.tools.list_ports.comports()
	ser = serial.Serial(com_ports[com_index].name)
	line = ser.readline()

	if create_local_db:
		patient_list = db.convert_to_patient_objects(line)
		for p in patient_list:
			db.save_patient(p)

	return eval(str(line)[1:].replace("\"", "").replace(r"\n", ""))




def get_patients():
	try:
		a = db.get_all_patients()

	except:
		a = read_patient(create_local_db = True)
		a = db.convert_to_patient_objects(a)
		for p in a:
			db.save_patient(p)

	return a




if __name__ == "__main__": #testing the function
	# print("waiting for patients")
	# patients = read_patient(com_index = 1)
	# print("GOT PATIENTS:")
	# print(patients)
	# print(type(patients))
	
	patients = {'Emre Cenk': {'Asprin': [(0, 0), (12, 0)], 'Talcid': [(17, 0), (17, 0)], 'Xanax': [(0, 0)], 'Beta': [(0, 0)]}, 'Alternative Cenk': {'Ibuprofen': [(0, 0), (12, 0)]}}
	
	for p in db.convert_to_patient_objects(patients):
		print(p.name, p.medications)



