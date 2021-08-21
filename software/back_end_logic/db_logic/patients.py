
from typing import Sequence

class TimeOfDay:

    def __init__(self, hour, minute):
        """Class to represent what time of day the medication will be taken at"""
        if hour == 0:
            self.hour = 24
        else:
            self.hour = hour
        self.minute = minute

# class medication():
#
#     def __init__(self, name, times):
#         self.name = name
#         self.times = times
#         self.last_taken = [False for i in range(len(times))]
#
#
class Patient:
    """A class that reperesents every patient"""

    def __init__(self, name, medication_list: Sequence[str], medication_times: Sequence[TimeOfDay]):

        # for every medication at index i, medication_times[i] is the time for that medication
        if len(medication_list) != len(medication_times):
            raise ValueError("Length of medications must be equal to length of medication_times. Otherwise we can't map a medication to a medication time")
        self.name = name


        # Mapping all of medication names to the medication times:
        self.medications = {} # {medication_Name: [ timeOfDay, TimeOfDay,], medication: [

        self.medications_last_taken = {} # keeping track of when the last time this specific medication was taken so that the person doesn't overdose

        for i in range(len(medication_list)):
            med_name = medication_list[i]
            med_time = medication_times[i]
            if med_name not in self.medications:
                self.medications[med_name] = [med_time]
            else:
                self.medications[med_name].append(med_time)

            if med_name not in self.medications_last_taken:
                self.medications_last_taken[med_name] = [None]
            else:
                self.medications_last_taken[med_name].append(None)

        """
        self.medications will have the following format: {"medname": [medication_time1, medicationtime2 ...], "medname2": [medtime1, medtime2...] ... }
        """


    def get_saveable_medication(self):
        medication_dict_to_save = {}
        for med in self.medications:
            time_list = []
            for i in range(len(self.medications[med])):
                #loopint through the medication times
                time_list.append((self.medications[med][i].hour, self.medications[med][i].minute))

            medication_dict_to_save[med] = time_list # Getting the hour and minute in a tuple: (hour, minute)


        return medication_dict_to_save

    def update_med_last_taken(self, med_name, index, force_update = False):
        from raspberrypi.main_loop import get_current_time, get_time_difference #this has to be here because you need to wait for both files to initialize

        current_time = get_current_time()
        if force_update:
            self.medications_last_taken[med_name][index] = current_time
            return True

        dif = get_time_difference(current_time, self.medications_last_taken[med_name][index])
        if dif > 12*60: #its been more than 24 hours:
            self.medications_last_taken[med_name][index] = current_time
            return True

        return False

    def can_patient_take_medication(self, med_name, index):
        if self.medications_last_taken[med_name][index] == None:
            self.update_med_last_taken(med_name, index, force_update = True)

            return True

        can_we_update = self.update_med_last_taken(med_name, index)
        return can_we_update #if it's been more than 24 hours, then the person can take it



class med_event():
    def __init__(self):
        self.med_name = ""
        self.patient_name = ""
        self.hour = 23
        self.minute = 12

output = [med_event(), med_event(), med_event()]