# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editingscreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
from software.back_end_logic.db_logic.db_utils import db
from typing import Sequence

class Ui_EditScreen(object):
	
	med_holder_styling = "background-color: #c4c4c4;\n"\
						 "color:black;\n"\
						 "border-style: outset;\n"\
						 "border-radius:15px;\n"\
						 "border-color: black;\n"\
						 "font: bold 14px;\n"\
						 "padding: 6px;\n"\
						 "min-width: 10px"\

	def customize_for_patient(self, full_patient_name: str):
		for i in reversed(range(self.vertical_layout_3_for_editing.count())):
			try:
				self.vertical_layout_3_for_editing.itemAt(i).widget().setParent(None)
			except:
				pass

		patients = db.get_all_patients()
		p_object = None
		for p in patients:                                                                      #Customizes the patients to be placed on the dashboard
			if p.name.lower() == full_patient_name.lower():
				p_object = p
				break

		if p_object is None:
			print("person does not exist")
			return

		self.MainName.setText(full_patient_name)

		for med in p_object.medications: # {medication_Name: [ timeOfDay, TimeOfDay,], medication: [
			self.add_medication(med_name = med, medication_times = p_object.medications[med])

		pix_map = QtGui.QPixmap(db.get_image(full_patient_name))
		pix_map = pix_map.scaledToHeight(200)
		self.userimage.setPixmap(pix_map)


	def add_current_med_in_gui(self):
		med_name = self.medication_input.text()
		if len(med_name) == 0:
			popup = QtWidgets.QMessageBox.question(self.EditScreen,
			                                       "",
			                                       "Medication Name cannot be empty",
			                                       QtWidgets.QMessageBox.Ok)
			return

		self.add_medication(med_name, [TimeOfDay(self.MedTime.time().hour(), self.MedTime.time().minute())])
		db.add_medication_to_patient(patient_name = self.MainName.text(), medication_times = [ TimeOfDay(self.MedTime.time().hour(), self.MedTime.time().minute()) ], medication_name = med_name)

	def add_medication(self, med_name: str, medication_times: Sequence[TimeOfDay]):




		medication_holder_template = QtWidgets.QWidget(self.medication_scroll_area)
		medication_holder_template.setStyleSheet(self.med_holder_styling)
		medication_holder_template.setObjectName("medication_holder_template")
		horizontalLayout_9 = QtWidgets.QHBoxLayout(medication_holder_template)
		horizontalLayout_9.setObjectName("horizontalLayout_9")


		med_name_label = QtWidgets.QLabel(medication_holder_template)
		font = QtGui.QFont()
		font.setPointSize(-1)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		med_name_label.setFont(font)
		med_name_label.setObjectName("Med_Quantity_6")
		horizontalLayout_9.addWidget(med_name_label)

		time_text = ""
		for t in medication_times:
			MedTime1_6 = QtWidgets.QLabel(medication_holder_template)
			font = QtGui.QFont()
			font.setPointSize(-1)
			font.setBold(True)
			font.setItalic(False)
			font.setWeight(75)
			MedTime1_6.setFont(font)
			MedTime1_6.setObjectName("MedTime1_6")


			minute = str(t.minute)
			if len(minute) == 1:
				minute = "0" + minute

			if t.hour <= 12:
				minute += " am"
			else:
				minute += " pm"
			MedTime1_6.setText(str(t.hour % 24) + "." + minute)
			horizontalLayout_9.addWidget(MedTime1_6)

		med_name_label.setText(med_name + ":")
		self.vertical_layout_3_for_editing.addWidget(medication_holder_template)

		self.vertical_layout_3_for_editing.removeItem(self.spacerItem3)
		self.vertical_layout_3_for_editing.addItem(self.spacerItem3)

	def go_back(self):
		self.stacked.setCurrentIndex(0)

	def setupUi2(self, EditScreen):
		self.EditScreen = EditScreen
		EditScreen.setObjectName("EditScreen")
		EditScreen.resize(1595, 944)
		self.gridLayout_6 = QtWidgets.QGridLayout(EditScreen)
		self.gridLayout_6.setObjectName("gridLayout_6")
		self.horizontalWidget = QtWidgets.QWidget(EditScreen)
		self.horizontalWidget.setMaximumSize(QtCore.QSize(16777215, 125))
		self.horizontalWidget.setStyleSheet("background-color: black")
		self.horizontalWidget.setObjectName("horizontalWidget")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_7 = QtWidgets.QLabel(self.horizontalWidget)
		self.label_7.setMaximumSize(QtCore.QSize(16777215, 100))
		self.label_7.setText("")
		self.label_7.setPixmap(QtGui.QPixmap(r"software/ui/profile.png"))
		self.label_7.setScaledContents(True)
		self.label_7.setObjectName("label_7")
		self.horizontalLayout_2.addWidget(self.label_7)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem)
		self.gobackbutton = QtWidgets.QToolButton(self.horizontalWidget)
		self.gobackbutton.clicked.connect(self.go_back)
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(15)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.gobackbutton.setFont(font)
		self.gobackbutton.setStyleSheet("background-color: #C4C4C4;\n"
"\n"
"border-style: outset;\n"
"border-radius:15px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.gobackbutton.setObjectName("gobackbutton")
		self.horizontalLayout_2.addWidget(self.gobackbutton)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
		self.gridLayout_6.addWidget(self.horizontalWidget, 0, 0, 1, 2)
		self.gridLayout_5 = QtWidgets.QGridLayout()
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.profileusername_2 = QtWidgets.QLabel(EditScreen)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_2.setFont(font)
		self.profileusername_2.setObjectName("profileusername_2")
		self.gridLayout_5.addWidget(self.profileusername_2, 1, 0, 1, 1)
		self.MainName = QtWidgets.QLabel(EditScreen)
		font = QtGui.QFont()
		font.setPointSize(21)
		font.setBold(True)
		font.setWeight(75)
		self.MainName.setFont(font)
		self.MainName.setObjectName("MainName")
		
		self.gridLayout_5.addWidget(self.MainName, 0, 0, 1, 1)
		self.dob = QtWidgets.QLabel(EditScreen)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.dob.setFont(font)
		self.dob.setObjectName("dob")
		self.gridLayout_5.addWidget(self.dob, 2, 1, 1, 1)
		
		
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)

		
		
		self.userimage = QtWidgets.QLabel(EditScreen)
		self.userimage.setText("")
		self.userimage.setPixmap(QtGui.QPixmap("someolddude.jpg"))
		self.userimage.setScaledContents(True)
		self.userimage.setObjectName("userimage")
		self.gridLayout_5.addWidget(self.userimage, 3, 0, 1, 1)
		self.age = QtWidgets.QLabel(EditScreen)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.age.setFont(font)
		self.age.setObjectName("age")
		self.gridLayout_5.addWidget(self.age, 1, 1, 1, 1)
		self.profileusername_4 = QtWidgets.QLabel(EditScreen)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_4.setFont(font)
		self.profileusername_4.setObjectName("profileusername_4")
		self.gridLayout_5.addWidget(self.profileusername_4, 4, 0, 1, 1)
		self.usernotes = QtWidgets.QTextEdit(EditScreen)
		self.usernotes.setObjectName("usernotes")
		self.gridLayout_5.addWidget(self.usernotes, 5, 0, 1, 2)
		self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 2, 1)
		self.gridWidget = QtWidgets.QWidget(EditScreen)
		self.gridWidget.setStyleSheet("background-color: #c4c4c4;\n"
"border-radius: 20%;")
		self.gridWidget.setObjectName("gridWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
		self.gridLayout.setObjectName("gridLayout")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.SaveButton = QtWidgets.QToolButton(self.gridWidget)
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(11)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.SaveButton.setFont(font)
		self.SaveButton.setStyleSheet("background-color: white;\n"
"\n"
"border-style: outset;\n"
"border-radius:15px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.SaveButton.setObjectName("SaveButton")
		self.horizontalLayout.addWidget(self.SaveButton)
		self.AddMed = QtWidgets.QToolButton(self.gridWidget)
		self.AddMed.clicked.connect(self.add_current_med_in_gui)
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(11)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.AddMed.setFont(font)
		self.AddMed.setStyleSheet("background-color: white;\n"
"\n"
"border-style: outset;\n"
"border-radius:15px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.AddMed.setObjectName("AddMed")
		self.horizontalLayout.addWidget(self.AddMed)
		self.RemoveMed = QtWidgets.QToolButton(self.gridWidget)
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(11)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.RemoveMed.setFont(font)
		self.RemoveMed.setStyleSheet("background-color: white;\n"
"\n"
"border-style: outset;\n"
"border-radius:15px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.RemoveMed.setObjectName("RemoveMed")
		self.horizontalLayout.addWidget(self.RemoveMed)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 5, 1, 1)
		self.profileusername_5 = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setPointSize(18)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_5.setFont(font)
		self.profileusername_5.setObjectName("profileusername_5")
		self.gridLayout.addWidget(self.profileusername_5, 0, 0, 1, 1)
		self.gridLayout_4 = QtWidgets.QGridLayout()
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.lineEdit_2 = QtWidgets.QLineEdit(self.gridWidget)
		self.lineEdit_2.setStyleSheet("background-color:white;\n"
"")
		self.lineEdit_2.setObjectName("lineEdit_2")
		self.gridLayout_4.addWidget(self.lineEdit_2, 0, 1, 1, 1)
		self.profileusername_6 = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_6.setFont(font)
		self.profileusername_6.setObjectName("profileusername_6")
		self.gridLayout_4.addWidget(self.profileusername_6, 1, 0, 1, 1)
		self.birthdate = QtWidgets.QDateEdit(self.gridWidget)
		self.birthdate.setStyleSheet("background-color: white;")
		self.birthdate.setObjectName("birthdate")
		self.gridLayout_4.addWidget(self.birthdate, 1, 1, 1, 1)
		self.profileusername_7 = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_7.setFont(font)
		self.profileusername_7.setObjectName("profileusername_7")
		self.gridLayout_4.addWidget(self.profileusername_7, 0, 0, 1, 1)
		self.changeimagebutton = QtWidgets.QToolButton(self.gridWidget)
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		font.setPointSize(15)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.changeimagebutton.setFont(font)
		self.changeimagebutton.setStyleSheet("background-color: white;\n"
"\n"
"border-style: outset;\n"
"border-radius:15px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.changeimagebutton.setObjectName("changeimagebutton")
		self.changeimagebutton.hide()


		self.gridLayout_4.addWidget(self.changeimagebutton, 2, 0, 1, 1)
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.TueCB = QtWidgets.QCheckBox(self.gridWidget)
		self.TueCB.setObjectName("TueCB")
		self.gridLayout_3.addWidget(self.TueCB, 0, 1, 1, 1)
		self.FriCB = QtWidgets.QCheckBox(self.gridWidget)
		self.FriCB.setObjectName("FriCB")
		self.gridLayout_3.addWidget(self.FriCB, 0, 4, 1, 1)
		self.WedCB = QtWidgets.QCheckBox(self.gridWidget)
		self.WedCB.setObjectName("WedCB")
		self.gridLayout_3.addWidget(self.WedCB, 0, 2, 1, 1)
		self.SatCB = QtWidgets.QCheckBox(self.gridWidget)
		self.SatCB.setObjectName("SatCB")
		self.gridLayout_3.addWidget(self.SatCB, 0, 5, 1, 1)
		self.ThuCB = QtWidgets.QCheckBox(self.gridWidget)
		self.ThuCB.setObjectName("ThuCB")
		self.gridLayout_3.addWidget(self.ThuCB, 0, 3, 1, 1)
		self.MonCB = QtWidgets.QCheckBox(self.gridWidget)
		self.MonCB.setObjectName("MonCB")
		self.gridLayout_3.addWidget(self.MonCB, 0, 0, 1, 1)
		self.SunCB = QtWidgets.QCheckBox(self.gridWidget)
		self.SunCB.setObjectName("SunCB")
		self.gridLayout_3.addWidget(self.SunCB, 1, 0, 1, 1)
		self.EveryCB = QtWidgets.QCheckBox(self.gridWidget)
		self.EveryCB.setObjectName("EveryCB")
		self.gridLayout_3.addWidget(self.EveryCB, 1, 1, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout_3, 2, 1, 1, 1)
		self.gridLayout.addLayout(self.gridLayout_4, 1, 0, 3, 1)
		self.formLayout = QtWidgets.QFormLayout()
		self.formLayout.setObjectName("formLayout")
		self.profileusername_8 = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_8.setFont(font)
		self.profileusername_8.setObjectName("profileusername_8")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.profileusername_8)
		self.MedTime = QtWidgets.QTimeEdit(self.gridWidget)
		self.MedTime.setStyleSheet("background-color:white;")
		self.MedTime.setObjectName("MedTime")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.MedTime)

		self.label = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setObjectName("label")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
		self.quantity = QtWidgets.QSpinBox(self.gridWidget)
		self.quantity.setStyleSheet("background-color:white;")
		self.quantity.setObjectName("quantity")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.quantity)
		self.medication_input = QtWidgets.QLineEdit(self.gridWidget)
		self.medication_input.setObjectName("medication_input")
		self.medication_input.setStyleSheet("background-color:white;")

		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.medication_input)
		self.profileusername_9 = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setBold(True)
		font.setWeight(75)
		self.profileusername_9.setFont(font)
		self.profileusername_9.setObjectName("profileusername_9")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.profileusername_9)
		self.gridLayout.addLayout(self.formLayout, 2, 5, 2, 1)
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
		self.gridLayout_6.addWidget(self.gridWidget, 2, 1, 1, 1)
		self.scrollArea = QtWidgets.QScrollArea(EditScreen)
		self.scrollArea.setStyleSheet("border-style: outset;\n"
"border-radius:10px;\n"
"border-color: black;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.medication_scroll_area = QtWidgets.QWidget()
		self.medication_scroll_area.setGeometry(QtCore.QRect(0, 0, 1139, 629))
		self.medication_scroll_area.setObjectName("medication_scroll_area")
		self.vertical_layout_3_for_editing = QtWidgets.QVBoxLayout(self.medication_scroll_area)
		self.vertical_layout_3_for_editing.setObjectName("vertical_layout_3_for_editing")
		self.label_4 = QtWidgets.QLabel(self.medication_scroll_area)
		font = QtGui.QFont()
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.label_4.setFont(font)
		self.label_4.setStyleSheet("background-color:transparent;")
		self.label_4.setObjectName("label_4")
		self.vertical_layout_3_for_editing.addWidget(self.label_4)





		self.spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.vertical_layout_3_for_editing.addItem(self.spacerItem3)

		self.scrollArea.setWidget(self.medication_scroll_area)
		self.gridLayout_6.addWidget(self.scrollArea, 1, 1, 1, 1)

		self.retranslateUi2(EditScreen)
		QtCore.QMetaObject.connectSlotsByName(EditScreen)

	def retranslateUi2(self, EditScreen):
		_translate = QtCore.QCoreApplication.translate
		EditScreen.setWindowTitle(_translate("EditScreen", "Dialog"))
		self.gobackbutton.setText(_translate("EditScreen", "Go Back"))
	
		
		
		
		self.profileusername_4.setText(_translate("EditScreen", "Notes:"))
		self.SaveButton.hide()
		self.AddMed.setText(_translate("EditScreen", "Add Med"))
		self.RemoveMed.setText(_translate("EditScreen", "Remove Med"))
		self.profileusername_5.setText(_translate("EditScreen", "Profile Edit"))
		
	
		self.changeimagebutton.setText(_translate("EditScreen", "Change Image"))
		self.TueCB.hide()
		self.FriCB.hide()
		self.WedCB.hide()
		self.SatCB.hide()
		self.lineEdit_2.hide()
		self.birthdate.hide()
		self.ThuCB.hide()
		self.MonCB.hide()
		self.SunCB.hide()
		self.EveryCB.hide()
		self.profileusername_8.setText(_translate("EditScreen", "Medication:"))
		self.label.setText(_translate("EditScreen", "Quantity:"))
		self.profileusername_9.setText(_translate("EditScreen", "Time:"))
		self.label_4.setText(_translate("EditScreen", "Medications"))
		



