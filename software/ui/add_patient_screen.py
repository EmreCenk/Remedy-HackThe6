
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QStackedLayout, QWidget, QApplication
from PyQt5 import QtGui, QtCore, QtWidgets
from software.back_end_logic.db_logic.patients import TimeOfDay, Patient
from software.back_end_logic.ai_logic.face_detection import take_pictures
from software.back_end_logic.db_logic.db_utils import db

class Window(QWidget):
	def __init__(self, function_to_call):
		super().__init__()

		self.function_to_call = function_to_call
		self.setWindowTitle("Add Patient")
		self.setWindowIcon(QtGui.QIcon("assets/logo.jfif"))
		p = self.palette()
		p.setColor(self.backgroundRole(), QtCore.Qt.white)
		self.setPalette(p)

		# Create a top-level layout
		layout = QVBoxLayout()
		self.setAutoFillBackground(False)
		self.setLayout(layout)
		# Create and connect the combo box to switch between pages



		self.stackedLayout = QStackedLayout()
		# Create the first page
		self.page1 = QWidget()
		self.page1Layout = QFormLayout()


		self.page1Layout.setVerticalSpacing(35)
		self.page1.setLayout(self.page1Layout)
		self.stackedLayout.addWidget(self.page1)


		# Create the second page
		self.page2 = QWidget()
		self.page2Layout = QFormLayout()
		self.page2Layout.setVerticalSpacing(15)

		self.page2.setLayout(self.page2Layout)
		self.stackedLayout.addWidget(self.page2)
		# Add the combo box and the stacked layout to the top-level layout
		layout.addLayout(self.stackedLayout)


		self.med_names = []
		self.med_times = []


		self.add_form()
	def add_form(self):
		self.name = QtWidgets.QLineEdit()
		self.page1Layout.addRow("Patient Name: ", self.name)

		self.medication_holder = QtWidgets.QVBoxLayout()

		self.medication_name = QtWidgets.QLineEdit()
		self.medication_time = QtWidgets.QTimeEdit()
		self.add_medication = QtWidgets.QPushButton()
		self.add_medication.setText("Add Medication")
		self.add_medication.clicked.connect(self.add_current_medication)
		a = QtWidgets.QHBoxLayout()
		a.addWidget(self.medication_name)
		a.addWidget(self.medication_time)
		a.addWidget(self.add_medication)

		self.page1Layout.addRow(self.medication_holder)
		self.page1Layout.addRow(a)

		self.finish_button = QtWidgets.QPushButton()
		self.finish_button.setText("Save Patient")
		self.finish_button.clicked.connect(self.finish)
		self.page1Layout.addRow(self.finish_button)

	def add_current_medication(self):
		current_med = self.medication_name.text()
		if current_med == "":
			alpha = QtWidgets.QMessageBox(self)
			alpha.setText(f"Medication cannot be empty")
			alpha.show()
			return

		min, hour = self.medication_time.time().minute(), self.medication_time.time().hour()

		med_label = QtWidgets.QLabel()
		med_label.setText("Medication: " + current_med + f"\nTime: {hour}, {min}\n\n")
		self.medication_holder.addWidget(med_label)

		self.med_names.append(current_med)
		self.med_times.append(TimeOfDay(hour = hour, minute = min))

	def finish(self):
		final_patient = Patient(name = self.name.text(), medication_list = self.med_names, medication_times = self.med_times)
		take_pictures(final_patient.name, how_many_pictures = 100)
		self.function_to_call(final_patient)
		self.close()

class alternative_window(Window):
        
	def emtpy(self):
		pass

	def add_form(self):
		pass
	def __init__(self):
		super().__init__(self.emtpy)
		
		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(20)
		
		self.name = QtWidgets.QLabel("To re-fill the dispenser when it is out of medicine:\n1) Open the dispenser via the button on the side\n2) Each Tube is labeled with a number. Fill the tube numbers with the following ")
		self.name.setFont(font)
		self.page1Layout.addRow(self.name)

		font.setPointSize(15)
		font.setWeight(1)

		meds = db.get_sorted_meds()
		for i in range(len(meds)):
			med = meds[i]
			curRow = QtWidgets.QLabel(f"Tube {i}: {med}")
			curRow.setFont(font)
			self.page1Layout.addRow(curRow)

		a = QtWidgets.QLabel()
		a.setFont(font)
		a.setText("\nAnd that's it, you are set for months of medication!\nEnjoy yourself!" )

		self.page1Layout.addRow(a)
if __name__ == '__main__':


	import sys
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec_())
