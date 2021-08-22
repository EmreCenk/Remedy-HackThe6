

from software.back_end_logic.db_logic.db_utils import db
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
import serial
import serial.tools.list_ports

def get_dict_to_send():

	all_patients = db.get_all_patients()
	dict_to_send = {}
	for i in range(len(all_patients)):
		dict_to_send[all_patients[i].name] = all_patients[i].get_saveable_medication()

	return dict_to_send

def upload_patients():
	to_send = str(get_dict_to_send()) + "\n"

	com_ports = serial.tools.list_ports.comports()
	for i in range(len(com_ports)): #we try to send it through every com port on the computer to make sure that the com port connected to the raspberry pi is sent
		try:
			s = serial.Serial(com_ports[i].name)
			s.write(to_send.encode())
		except:
			pass #this is fine


if __name__ == '__main__':
	import os
	current_dir = os.getcwd()
	os.chdir(current_dir.replace("software\serial_comm", "")) # updating the working directory (since everything will be called from the parent Meddis directory)


	upload_patients()