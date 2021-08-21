

"""Database Utility Functions (aka a bunch of text files)

The json format for the data storage of patients will be the following:

patients = { "Patient Name": {"medication": ["med1", "med2", "med3"...],

"""
from software.back_end_logic.db_logic.patients import Patient, TimeOfDay
from typing import List, Tuple
import os

default_path_to_save = "patient_db.txt"
sepcha = "\n\nseparating_now\n\n" #separating character between patients

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

    @staticmethod
    def remove_patient(patient_name: str) -> None:

        """Deletes a patients from the database"""


        #Deleting patient profile:
        patients = db.get_all_patients()

        file = open(default_path_to_save, "w")
        file.write("") #overwriting file
        file.close()

        for p in patients:
            if p.name == patient_name:
                continue
            db.save_patient(p)

        #Deleting patient pictures:
        try:
            image_path = os.path.join(os.getcwd(), "software", "back_end_logic", "ai_logic", "images", patient_name)
            original_cwd = os.getcwd()
            os.chdir(image_path)
            for file in os.listdir():
                os.remove(file)

            os.chdir(original_cwd)
            os.rmdir(image_path)

        except:
            pass #The user is from a previous version of the program when the imagse of the person was not saved from the ui yet. This is fine.



    @staticmethod
    def get_image(patient_name):
        original_dir = os.getcwd()
        image_path = os.path.join(original_dir, "software", "back_end_logic", "ai_logic", "images")
        os.chdir(image_path)
        name_to_go = None
        for name in os.listdir():
            if patient_name.lower() == name.lower():
                name_to_go = name

        if name_to_go is None:
            os.chdir(original_dir)
            return None

        current_path = os.path.join(image_path, name_to_go)
        os.chdir(current_path)
        path_to_return = os.path.join(current_path, os.listdir()[0])
        os.chdir(original_dir)

        return path_to_return
    @staticmethod
    def add_medication_to_patient(patient_name: str, medication_name: str, medication_times: List[TimeOfDay]) -> None:
        """Adds a medication to the database for a specific patient"""

        patients = db.get_all_patients()

        file = open(default_path_to_save, "w")
        file.write("") #overwriting file
        file.close()

        for p in patients:
            if p.name == patient_name:
                if medication_name in p.medications:
                    for specific_time in medication_times:
                        print(specific_time.hour, specific_time.minute)
                        p.medications[medication_name].append(specific_time)

                else:
                    p.medications[medication_name] = medication_times
            db.save_patient(p)


    @staticmethod
    def get_sorted_meds(patient_list = None):
        if patient_list is None:
            patient_list = db.get_all_patients()

        all_meds = []
        for p in patient_list:
            for med in p.medications:
                if med not in all_meds:
                    all_meds.append(med)

        all_meds.sort()
        return all_meds



if __name__ == '__main__':
    #Testing the db class:
    # from back_end_logic.patients import Patient, TimeOfDay
    # patient1 = Patient(name = "Example Patient1", medication_list = ["Xanax", "SomeMed"], medication_times = [TimeOfDay(1, 23), TimeOfDay(3, 2)])
    # db.save_patient(patient1)
    #
    # patient1 = Patient(name = "Example Patient1", medication_list = ["Xanax", "SomeMed"], medication_times = [TimeOfDay(1, 23), TimeOfDay(3, 2)])
    # db.save_patient(patient1)
    #
    #
    # patient1 = Patient(name = "Example Patient2", medication_list = ["Xanax", "SomeMed"], medication_times = [TimeOfDay(1, 23), TimeOfDay(3, 2)])
    # db.save_patient(patient1)
    #
    # #print()

    db.add_medication_to_patient("Example Patient2", "adding a medication", [TimeOfDay(16, 12), TimeOfDay(16, 13)])


    db.remove_patient("Example Patient1")

