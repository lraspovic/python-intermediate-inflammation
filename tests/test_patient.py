"""Tests for the Patient model."""


def test_create_patient():
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)

    assert p.name == name

def test_create_doctor():
    from inflammation.models import Doctor
    name = 'Mr Doc'
    doc = Doctor(name)
    assert name == doc.name

def test_doctor_is_a_person():
    from inflammation.models import Doctor, Person
    doc = Doctor('Mr Doc')
    assert isinstance(doc, Person)

def test_patients_added_correctly():
    from inflammation.models import Patient, Doctor
    alice = Patient('Alice')
    doc = Doctor('Mr Doc')
    doc.add_patient(alice)
    assert doc.patients is not None
    assert len(doc.patients) == 1

def test_no_duplicate_patients():
    from inflammation.models import Patient, Doctor
    alice = Patient('Alice')
    doc = Doctor('Mr Doc')
    doc.add_patient(alice)
    doc.add_patient(alice)
    assert len(doc.patients) == 1