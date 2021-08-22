


import serial
import serial.tools.list_ports

def read_patient(com_index = 0):
	com_ports = serial.tools.list_ports.comports()
	ser = serial.Serial(com_ports[com_index].name)
	line = ser.readline()

	return eval(str(line))



print("waiting for patients")
patients = read_patient(com_index = 1)
print("GOT PATIENTS:")
print(patients)
print(type(patients))