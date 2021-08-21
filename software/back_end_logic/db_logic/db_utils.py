

"""Database Utility Functions (aka a bunch of text files)

The json format for the data storage of patients will be the following:

patients = { "Patient Name": {"medication": ["med1", "med2", "med3"...],

"""
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
from typing import List, Tuple
import os

default_path_to_save = "patient_db.txt"
sepcha = "\n\nseparating_now\n\n"

class db():

    @staticmethod
    def save_patient(patient_object: Patient, path_to_save = None) -> None:
        """Saves the patient onto the drive"""
        global default_path_to_save, sepcha

        if path_to_save is None:
            path_to_save = default_path_to_save

        what_to_save = {patient_object.name: patient_object.get_saveable_medication()}

        file = open(path_to_save, "a+")

        file.write(str(what_to_save) + sepcha) # "\n" is the separator character between patients

        file.close()

    @staticmethod
    def get_all_patients(path_to_read = None) -> List[Patient]:
        """
        Gets all patients that are saved into the databse.
        :return: a list of Patient objects
        """

        global default_path_to_save, sepcha
        if path_to_read is None:
            path_to_read = default_path_to_save

        #opening and reading file:
        #print(os.getcwd())
        file = open(path_to_read, "r")
        text_to_parse = file.read()
        file.close()

        #parsing text:
        text_to_parse = text_to_parse.split(sepcha)

        patients = {}
        for p in text_to_parse:
            if len(p) < 2:
                continue

            p_dict = eval(p) #dictionary of the person
            if len(patients) == 0:
                patients = p_dict # python reads the dictionary we saved with the eval() function
                #print(len(p_dict))
                continue

            for name in p_dict:
                patients[name] = p_dict[name]

        #print(patients)
        return db.convert_to_patient_objects(patients)

    @staticmethod
    def convert_to_patient_objects(dict_to_convert: dict[str: dict[str:  List[Tuple[int, int]]]]    ) -> List[Patient]:
        """Takes a dictionary (which is read from the databse), and converts that dictionary to a list of patient objects."""

        patient_list = []
        for name in dict_to_convert:
            medication_times = []
            medication_names = []
            for med_name in dict_to_convert[name]:
                for med_time in dict_to_convert[name][med_name]:
                    medication_times.append(TimeOfDay(med_time[0], med_time[1]))
                    medication_names.append(med_name)
            patient_list.append(
                Patient(name = name, medication_list = medication_names, medication_times = medication_times)
            )

        return patient_list


