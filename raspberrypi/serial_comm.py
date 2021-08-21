import serial
from typing import Sequence, List
from software.back_end_logic.db_logic.db_utils import db
from threading import Thread
from time import sleep
import serial.tools.list_ports

class communicator():

	def __init__(self, COM_PORT_NAME = ""):
		ports = serial.tools.list_ports.comports()

		if COM_PORT_NAME == "":
			self.all_ports = []
			print("PORTS:")
			for i in range(len(ports)):
				print(ports[i].name)
				try:
					port_name = ports[i].name
					current_port = serial.Serial(port_name, baudrate = 9600)
					self.all_ports.append(current_port)

					#try not indenting this and see if it works:
					sleep(2)
				except:
					pass #this is fine, it just couldn't open the com port. We are good

			for i in [5,6,7]:
				try:
					port_name = "COM"+str(i)
					self.all_ports.append(serial.Serial(port_name, baudrate=9600))
					print(port_name)
				except Exception as E:
					print("error: " + str(E))
					print("couldn't open port: " + port_name)

		else:
			self.all_ports = [serial.Serial(COM_PORT_NAME, baudrate = 9600)]
			sleep(2)



	def send_to_arduino(self, infoReceived):
		for arduinoSerial in self.all_ports:
			print("sent ", infoReceived, "to", arduinoSerial.name)
			try:
				arduinoSerial.write(infoReceived.encode())
			except:
				print("Couldn't send to port: " + arduinoSerial.name)





	def send_all_meds_to_arduino_with_thread(self, list_of_meds: Sequence[str]):

		myThread = Thread(target = lambda: self.sar(list_of_meds))
		myThread.start()



	def sar(self, list_of_meds: Sequence[str]):
		#sends meds to arduino
		medication_indexes = db.get_sorted_meds()
		# self.send_to_arduino("g")
		for m in list_of_meds:
			self.send_to_arduino("g" + str(medication_indexes.index(m)) + "1")
			sleep(1) #Wait for arduino to process input

if __name__ == '__main__':
	a = communicator()
	a.send_to_arduino("g11")
	# a.send_to_arduino("g")
	# sleep(0.1)
	# a.send_to_arduino("1")
	# sleep(0.1)
	# a.send_to_arduino("1")
	# a.send_to_arduino("1")
	# sleep(1)
	#
	# a = serial.Serial("COM7", baudrate=9600)
	# sleep(1)
	#
	# a.write(b'g11')
	# sleep(1)
	#
	# print("sent")