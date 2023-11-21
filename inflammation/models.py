"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains 
inflammation data for a single patient taken over a number of days 
and each column represents a single day across all patients.
"""

import numpy as np


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflamation data (each row contains measurements for a single patient across all days).
    :returns: An array of mean values of measurements for each day.
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflamation data (each row contains measurements for a single patient across all days).
    :returns: An array of max values of measurements for each day.
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array for each day.
    
    :param data: A 2D data array with inflamation data (each row contains measurements for a single patient acrossa all days).
    :returns: An array of minimum values of measurements for each day.
    """
    return np.min(data, axis=0)

def patient_normalise(data):
    """Normalise patient data from a 2D inflammation data array.

    NaN values are ignored, and normalised to 0.

    Negative values are rounded to 0.
    """
    if not isinstance(data, np.ndarray):
        raise TypeError('data input should be ndarray')
    if len(data.shape) != 2:
        raise ValueError('inflammation array should be 2-dimensional')
    if np.any(data < 0):
        raise ValueError('Inflamation values sholud not be negative')

    max_data = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data / max_data[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised

def daily_stdev(data):
    """Calculate the daily standard deviation of a 2D inflammation data array for each day.

    :param data: A 2D data array with inflammation data (each row contanins measuremetns for a single patient across all days).
    :returns: An array of stdev values of measurements for each day.
    """

    return np.std(data, axis=1)

def daily_above_treshold(patient_num, data, treshold):
    """Determine whether or not each daily inflammation value exceeds a given treshold for a given patient.

    :param patient_num: The patient row number
    :param data: A 2D data array with inflammation data
    :param treshold: An inflammation treshold to check each daily value against
    :returns: A boolean list representing whether or not each patient's daily inflammation exceeded the treshold
    """ 

    bool_array = list(map(lambda x: x > treshold, data[patient_num]))
    from functools import reduce

    return reduce(lambda a, b: a + b, [1 for day in bool_array if day])

class Observation:
    def __init__(self, day, value):
        self.day = day
        self.value = value
    
    def __str__(self) -> str:
        return str(self.value)

class Person:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

class Patient(Person):
    """A patient in an inflammation study."""
    def __init__(self, name, observations=None) -> None:
        super().__init__(name)
        self.observations = []

        if observations is not None:
            self.observations = observations

    def add_observation(self, value, day=None):
        if day is None:
            try: 
                day = self.observations[-1].day + 1

            except IndexError:
                day = 0
        
        new_observation = Observation(day, value)

        self.observations.append(new_observation)
        return new_observation
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def last_observation(self):
        return self.observations[-1]

class Doctor(Person):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.patients = []
    
    def add_patient(self, patient):
        if not patient in self.patients:
            self.patients.append(patient)