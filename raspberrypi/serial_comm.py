import serial
from typing import Sequence
from software.back_end_logic.db_logic.db_utils import db
from threading import Thread
from time import sleep
import serial.tools.list_ports

class communicator():

	def __init__(self, COM_PORT_NAME = ""):
		ports = serial.tools.list_ports.comports()
		self.sleep_between_time = 0.5
		if COM_PORT_NAME == "":
			self.all_ports = []

			for i in range(len(ports)):
				try:
					port_name = ports[i].name
					current_port = serial.Serial(port_name, baudrate = 9600)
					self.all_ports.append(current_port)

					#try not indenting this and see if it works:
					sleep(2)
				except:
					pass #this is fine, it just couldn't open the com port. We are good


		else:
			self.all_ports = [serial.Serial(COM_PORT_NAME, baudrate = 9600)]
			sleep(2)

		self.intialize_with_arduino()


	def send_to_arduino(self, infoReceived):
		for arduinoSerial in self.all_ports:
			try:
				arduinoSerial.write(infoReceived.encode())
			except:
				print("Couldn't send to port: " + arduinoSerial.name)



	def intialize_with_arduino(self):
		print("sending 'g00' to initialize")
		self.send_to_arduino(("g"))
		sleep(self.sleep_between_time)
		self.send_to_arduino(("0"))
		sleep(self.sleep_between_time)
		self.send_to_arduino(("0"))



	def send_all_meds_to_arduino_with_thread(self, list_of_meds: Sequence[str]):

		myThread = Thread(target = lambda: self.sar(list_of_meds))
		myThread.start()



	def sar(self, list_of_meds: Sequence[str]):
		print("Sending medications to arduino")
		#sends meds to arduino
		medication_indexes = db.get_sorted_meds()
		already_sent = set()
		for m in list_of_meds:
			if m in already_sent:
				continue

			print("sending: " + "g"+str(medication_indexes.index(m))+str(list_of_meds.count(m)))
			#sending the "g" element
			self.send_to_arduino("g")
			sleep(self.sleep_between_time)
			print('sent: ' + "g")
			#sending the "x" element
			self.send_to_arduino(str(medication_indexes.index(m)))
			sleep(self.sleep_between_time)
			print("sent: " + str(medication_indexes.index(m)))
			#sending the y element
			self.send_to_arduino(str(list_of_meds.count(m)))
			print("sent: " + str(list_of_meds.count(m)))
			already_sent.add(m)
			print()
			sleep(5) #Wait for arduino to process input

if __name__ == '__main__':
	a = communicator()
	a.send_to_arduino("g")
	a.send_to_arduino("d")