"""Module containing code for plotting inflammation data."""

from matplotlib import pyplot as plt
import numpy as np
from inflammation.serializers import PatientJSONSerializer


def visualize(data_dict):
    """Display plots of basic statistical properties of the inflammation data.

    :param data_dict: Dictionary of name -> data to plot
    """
    # TODO(lesson-design) Extend to allow saving figure to file
    num_plots = len(data_dict)
    fig = plt.figure(figsize=((3 * num_plots) + 1, 3.0))

    for i, (name, data) in enumerate(data_dict.items()):
        axes = fig.add_subplot(1, num_plots, i + 1)

        axes.set_ylabel(name)
        axes.plot(data)

    fig.tight_layout()

    plt.show()

def display_patient_record(patient):
    """Display data for a single patient."""
    print(patient.name)
    for obs in patient.observations:
        print(obs.day, obs.value)

def save_patient_record(patient, save_path):
    if not isinstance(patient, list):
        patient = [patient]
    PatientJSONSerializer.save(patient, save_path)