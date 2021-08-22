

from PyQt5 import QtCore, QtGui, QtWidgets
from software.back_end_logic.db_logic.db_utils import db
from software.ui.add_patient_screen import Window, alternative_window
from software.back_end_logic.db_logic.patients import Patient
from software.back_end_logic.ai_logic.training_faces import train_model
from software.ui.editing_screen import Ui_EditScreen
class Ui_Dialog(Ui_EditScreen):
	patient_button_styling = "background-color: white;\n"\
		                          "color:black;\n"\
		                          "border-style: outset;\n"\
		                          "border-radius:10px;\n"\
		                          "border-color: black;\n"\
		                          "font: bold 25px;\n"\
		                          "padding: 6px;\n"\
		                          "min-width: 10px;\n"\
		                          "height: 30%;"
	highlighted_patient_button_styling = "background-color: yellow;\n"\
		                          "color:black;\n"\
		                          "border-style: outset;\n"\
		                          "border-radius:10px;\n"\
		                          "border-color: black;\n"\
		                          "font: bold 25px;\n"\
		                          "padding: 6px;\n"\
		                          "min-width: 10px;\n"\
		                          "height: 30%;"
	button_styling = "background-color: white;\n"\
	                 "\n"\
	                 "border-style: outset;\n"\
	                 "border-radius:15px;\n"\
	                 "border-color: black;\n"\
	                 "padding: 6px;\n"\
	                 "min-width: 10px"

	overview_text_styling = "font: bold 25px;"



	def __init__(self, Dialog):
		self.stacked = QtWidgets.QStackedLayout()
		dialog2 = QtWidgets.QWidget()
		self.setupUi2(dialog2)
		self.setupUi(Dialog)
		self.Dialog = Dialog
		
		self.stacked.addWidget(Dialog)
		self.stacked.addWidget(dialog2)

		self.previous_pressed_button_index = None # stores the previously stored button's index so we can un-highlight it
		self.patient_button_list = [] # Stores a list of buttons that hold the patients in the scrollarea (each button in the scrollarea will be an entry in this list)
		self.update_scrollbar()
	def update_scrollbar(self):

		for i in range(len(self.patient_button_list)):

			self.verticalLayout_3.removeWidget(self.patient_button_list[i])
			self.patient_button_list[i].deleteLater()
			self.patient_button_list[i] = None

		self.patient_button_list = []
		self.patients = db.get_all_patients() #reads list of patients from database
		self.add_patients_from_db()

	def add_patients_from_db(self):
		for p in self.patients:
			self.add_patient_to_scrollarea(p.name)

	def add_patient_to_scrollarea(self, patient_name: str):
		patient_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		patient_button.setStyleSheet(self.patient_button_styling)
		patient_button.setText(patient_name)
		patient_index = len(self.patient_button_list)
		patient_button.clicked.connect(lambda: self.update_overview(patient_index = patient_index)) # the button gives what index it is at to the update_overview method

		self.patient_button_list.append(patient_button) #adding the button to our button list so that we can access it later

		self.verticalLayout_3.addWidget(patient_button)
		self.verticalLayout_3.removeItem(self.spacerItem)
		self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(self.spacerItem)


	def update_overview(self, patient_index):
		if self.previous_pressed_button_index is not None:
			try:
				previous_button = self.patient_button_list[self.previous_pressed_button_index]
				previous_button.setStyleSheet(self.patient_button_styling)
			except:
				pass # this is like the dog in the burning house meme: "this is fine."

		button_pressed = self.patient_button_list[patient_index]
		button_pressed.setStyleSheet(self.highlighted_patient_button_styling)

		patient_object = self.patients[patient_index]
		self.profile_label_1.setText("Name: " + patient_object.name)
		self.profile_label_2.setText("Known Medications: ")

		text_to_save = ""
		meds = patient_object.get_saveable_medication()
		i = 1
		for med in meds:
			to_save = ""
			for time_ in meds[med]:
				to_save += str(time_[0]) + ". " + str(time_[1]) + ",       "

			to_save = to_save[:-len(",       ")]
			text_to_save += str(i) + ") " + med + " Time: " + to_save + "\n"
			i += 1

		self.profile_label_3.setText(text_to_save)
		self.previous_pressed_button_index = patient_index

	def save_and_update(self, patient: Patient):
		db.save_patient(patient)
		train_model() # re-training the model so they recognize the current user as well
		self.update_scrollbar()

	def display_add_new_screen(self):
		self.new_window = Window(self.save_and_update)
		self.new_window.show()

	def delete_current_user(self):
		if self.previous_pressed_button_index is None:
			return
		popup = QtWidgets.QMessageBox.question(self.Dialog,
		                                       "",
		                                       "Are you sure you want to delete this user: " + self.patients[self.previous_pressed_button_index].name + "?\nThis action is permanent.",
		                                       QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes, )

		if popup != QtWidgets.QMessageBox.Yes:
			return

		db.remove_patient(self.patients[self.previous_pressed_button_index].name)
		self.update_scrollbar()

	def move_patient_cursor(self, direction: int):
		if self.previous_pressed_button_index is None:
			update_index = 0
		else:
			update_index = (self.previous_pressed_button_index - direction) % len(self.patients)
		self.update_overview(update_index)

	def view_profile(self):
		if self.previous_pressed_button_index is None:
			return

		self.customize_for_patient(self.patient_button_list[self.previous_pressed_button_index].text())
		self.stacked.setCurrentIndex(1)
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(1366, 768)
		font = QtGui.QFont()
		Dialog.setFont(font)

		self.gridLayout = QtWidgets.QGridLayout(Dialog)
		self.gridLayout.setObjectName("gridLayout")
		self.gridWidget = QtWidgets.QWidget(Dialog)
		self.gridWidget.setStyleSheet("background-color: #c4c4c4;\n"
"border-radius: 20%;")
		self.gridWidget.setObjectName("gridWidget")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.gridWidget)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.profile_label_3 = QtWidgets.QLabel(self.gridWidget)
		self.profile_label_3.setObjectName("profile_label_3")
		self.gridLayout_3.addWidget(self.profile_label_3, 4, 2, 1, 1)
		self.profile_label_1 = QtWidgets.QLabel(self.gridWidget)
		self.profile_label_1.setObjectName("profile_label_1")
		self.gridLayout_3.addWidget(self.profile_label_1, 2, 2, 1, 1)
		self.profile_label_2 = QtWidgets.QLabel(self.gridWidget)
		self.profile_label_2.setObjectName("profile_label_2")
		self.gridLayout_3.addWidget(self.profile_label_2, 3, 2, 1, 1)
		# self.profile_label_4 = QtWidgets.QLabel(self.gridWidget)
		# self.profile_label_4.setObjectName("profile_label_4")
		# self.gridLayout_3.addWidget(self.profile_label_4, 5, 2, 1, 1)
		# self.profile_label_5 = QtWidgets.QLabel(self.gridWidget)
		# self.profile_label_5.setObjectName("profile_label_5")
		# self.gridLayout_3.addWidget(self.profile_label_5, 6, 2, 1, 1)
		self.overview_label = QtWidgets.QLabel(self.gridWidget)
		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(20)
		font.setBold(True)
		font.setWeight(75)
		self.overview_label.setFont(font)
		self.overview_label.setObjectName("overview_label")
		self.gridLayout_3.addWidget(self.overview_label, 1, 2, 1, 1)
		self.gridLayout.addWidget(self.gridWidget, 1, 0, 1, 2)
		self.verticalWidget = QtWidgets.QWidget(Dialog)
		self.verticalWidget.setMaximumSize(QtCore.QSize(400, 16777215))
		self.verticalWidget.setObjectName("verticalWidget")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.scrollArea = QtWidgets.QScrollArea(self.verticalWidget)
		self.scrollArea.setStyleSheet("background-color: #c4c4c4;\n"
"border-radius: 45%;")
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName("scrollArea")
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 382, 567))
		self.scrollAreaWidgetContents.setObjectName("medication_scroll_area")
		self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
		self.verticalLayout_3.setObjectName("vertical_layout_3_for_editing")
		self.patients_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(20)
		font.setBold(True)
		font.setWeight(75)
		self.patients_label.setFont(font)
		self.patients_label.setStyleSheet("background-color:transparent;")
		self.patients_label.setObjectName("patients_label")
		self.verticalLayout_3.addWidget(self.patients_label)

		self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(self.spacerItem)

		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.verticalLayout_2.addWidget(self.scrollArea)
		self.gridLayout.addWidget(self.verticalWidget, 1, 2, 2, 1)
		self.gridWidget1 = QtWidgets.QWidget(Dialog)
		self.gridWidget1.setStyleSheet("background-color: #c4c4c4;\n"
"border-radius: 25%;")
		self.gridWidget1.setObjectName("gridWidget1")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.gridWidget1)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.move_up_arrow_button = QtWidgets.QToolButton(self.gridWidget1)
		self.move_up_arrow_button.clicked.connect(lambda: self.move_patient_cursor(1))

		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(15)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.move_up_arrow_button.setFont(font)
		self.move_up_arrow_button.setStyleSheet(self.button_styling)
		self.move_up_arrow_button.setObjectName("move_up_arrow_button")
		self.gridLayout_4.addWidget(self.move_up_arrow_button, 0, 2, 1, 1)
		self.delete_user_button = QtWidgets.QToolButton(self.gridWidget1)
		self.delete_user_button.clicked.connect(self.delete_current_user)
		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(8)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.delete_user_button.setFont(font)
		self.delete_user_button.setStyleSheet(self.button_styling)
		self.delete_user_button.setObjectName("delete_user_button")
		self.gridLayout_4.addWidget(self.delete_user_button, 0, 1, 1, 1)
		self.move_down_arrow_button = QtWidgets.QToolButton(self.gridWidget1)
		self.move_down_arrow_button.clicked.connect(lambda: self.move_patient_cursor(-1))

		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(15)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.move_down_arrow_button.setFont(font)
		self.move_down_arrow_button.setStyleSheet(self.button_styling)
		self.move_down_arrow_button.setObjectName("move_down_arrow_button")
		self.gridLayout_4.addWidget(self.move_down_arrow_button, 0, 3, 1, 1)
		self.view_profile_button = QtWidgets.QToolButton(self.gridWidget1)
		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(8)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.view_profile_button.setFont(font)
		self.view_profile_button.setStyleSheet(self.button_styling)
		self.view_profile_button.setObjectName("view_profile_button")
		self.view_profile_button.clicked.connect(self.view_profile)
		self.gridLayout_4.addWidget(self.view_profile_button, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.gridWidget1, 2, 1, 1, 1)
		self.horizontalWidget = QtWidgets.QWidget(Dialog)
		self.horizontalWidget.setMaximumSize(QtCore.QSize(16777215, 125))
		self.horizontalWidget.setStyleSheet("background-color: black")
		self.horizontalWidget.setObjectName("horizontalWidget")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_2 = QtWidgets.QLabel(self.horizontalWidget)
		self.label_2.setMaximumSize(QtCore.QSize(16777215, 100))
		self.label_2.setText("")
		self.label_2.setPixmap(QtGui.QPixmap(r"software\ui\logo.jpg"))
		self.label_2.setScaledContents(True)
		self.label_2.setObjectName("label_2")
		self.horizontalLayout_2.addWidget(self.label_2)
		spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
		self.add_new_button = QtWidgets.QToolButton(self.horizontalWidget)
		self.add_new_button.clicked.connect(self.display_add_new_screen)


		font = QtGui.QFont()
		font.setFamily("Arial Black")
		font.setPointSize(15)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)

		self.see_what_to_fill = QtWidgets.QToolButton(self.horizontalWidget)
		self.see_what_to_fill.clicked.connect(self.see_med_indexes)
		self.see_what_to_fill.setFont(font)
		self.see_what_to_fill.setStyleSheet(self.button_styling)
		self.see_what_to_fill.setText("How To Fill The Dispenser")
		self.horizontalLayout_2.addWidget(self.see_what_to_fill)


		self.add_new_button.setFont(font)
		self.add_new_button.setStyleSheet(self.button_styling)
		self.add_new_button.setObjectName("add_new_button")
		self.horizontalLayout_2.addWidget(self.add_new_button)
		spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem2)
		self.gridLayout.addWidget(self.horizontalWidget, 0, 0, 1, 3)
		self.emergency_stop_button = QtWidgets.QPushButton(Dialog)
		self.emergency_stop_button.setMinimumSize(QtCore.QSize(22, 40))
		font = QtGui.QFont()
		font.setPointSize(-1)
		font.setBold(True)
		font.setItalic(False)
		font.setWeight(75)
		self.emergency_stop_button.setFont(font)
		self.emergency_stop_button.setStyleSheet(
"color:white;\n"
"border-style: outset;\n"
"border-radius:10px;\n"
"border-color: black;\n"
"font: bold 14px;\n"
"padding: 6px;\n"
"min-width: 10px")
		self.emergency_stop_button.setObjectName("emergency_stop_button")
		self.gridLayout.addWidget(self.emergency_stop_button, 2, 0, 1, 1)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def see_med_indexes(self):
		self.new_window = alternative_window()
		self.new_window.show()

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
		self.profile_label_1.setStyleSheet(self.overview_text_styling)
		self.profile_label_2.setStyleSheet(self.overview_text_styling)
		self.profile_label_3.setStyleSheet(self.overview_text_styling)
		# self.profile_label_4.setStyleSheet(self.overview_text_styling)
		# self.profile_label_5.setStyleSheet(self.overview_text_styling)

		self.profile_label_1.setText(_translate("Dialog", "Name"))
		self.profile_label_2.setText(_translate("Dialog", "Known Medications:"))
		self.profile_label_3.setText(_translate("Dialog", "Medications"))
		# self.profile_label_4.setText(_translate("Dialog", "other2"))
		# self.profile_label_5.setText(_translate("Dialog", "other3"))
		self.overview_label.setText(_translate("Dialog", "Overview"))
		self.patients_label.setText(_translate("Dialog", "Patients"))
		self.move_up_arrow_button.setText(_translate("Dialog", "↑"))
		self.delete_user_button.setText(_translate("Dialog", "Delete User"))
		self.move_down_arrow_button.setText(_translate("Dialog", "↓"))
		self.view_profile_button.setText(_translate("Dialog", "View Profile"))
		self.add_new_button.setText(_translate("Dialog", "  Add New  "))
		
