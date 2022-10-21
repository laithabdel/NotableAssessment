import json
from unittest.mock import patch, MagicMock

from django.test import TestCase
from datetime import datetime, timezone
from app.models import Doctor, Patient, Appointment
from app.services import DoctorService, CalendarService
from django.urls import reverse


class DoctorCreationTestCase(TestCase):
    def test_create_doctor(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        self.assertEqual(doctor.first_name, 'Bob')
        self.assertEqual(doctor.last_name, 'Dylan')


class PatientCreationTestCase(TestCase):
    def test_create_patient(self):
        patient = Patient(first_name='Alex', last_name='Mitchell')
        patient.save()
        self.assertEqual(patient.first_name, 'Alex')
        self.assertEqual(patient.last_name, 'Mitchell')


class AppointmentCreationTestCase(TestCase):
    def test_create_appointment(self):
        patient = Patient(first_name='Alex', last_name='Mitchell')
        patient.save()
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        date_time = datetime.now()
        appointment = Appointment(doctor=doctor, patient=patient, appointment_datetime=date_time,
                                  appointment_type="New Patient")
        appointment.save()
        self.assertEqual(appointment.doctor, doctor)
        self.assertEqual(appointment.patient, patient)
        self.assertEqual(appointment.appointment_datetime, date_time)
        self.assertEqual(appointment.appointment_type, "New Patient")


class DoctorServiceTestCase(TestCase):
    def test_get_doctors(self):
        Doctor(first_name='Bob', last_name='Dylan').save()
        Doctor(first_name='Mike', last_name='Dane').save()
        Doctor(first_name='John', last_name='Doe').save()

        doctors = DoctorService.get_doctors()
        expected_result = [
            {'id': 1, 'first_name': 'Bob', 'last_name': 'Dylan'},
            {'id': 2, 'first_name': 'Mike', 'last_name': 'Dane'},
            {'id': 3, 'first_name': 'John', 'last_name': 'Doe'}
        ]
        self.assertEqual(doctors, expected_result)


class CalendarServiceTestCase(TestCase):
    def test_get_appointments(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        patient = Patient(first_name="John", last_name="Brown")
        patient.save()
        date_time = datetime(2022, 10, 1, tzinfo=timezone.utc)
        appointment = Appointment(doctor=doctor, patient=patient, appointment_datetime=date_time,
                                  appointment_type="New Patient")
        appointment.save()

        result = CalendarService.get_appointments(doctor.id, date_time)
        expected_result = [{'id': appointment.id, 'doctor_id': 1, 'patient_id': 1, 'appointment_datetime': date_time,
                            'appointment_type': 'New Patient'}]
        self.assertEqual(result, expected_result)

    def test_delete_appointments(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        patient = Patient(first_name="John", last_name="Brown")
        patient.save()
        date_time = datetime(2022, 10, 1, tzinfo=timezone.utc)
        appointment = Appointment(doctor=doctor, patient=patient, appointment_datetime=date_time,
                                  appointment_type="New Patient")
        appointment.save()

        current_state = Appointment.objects.all().count()
        self.assertEqual(1, current_state)

        CalendarService.delete_appointment(appointment.id)

        result = Appointment.objects.all().count()
        self.assertEqual(result, 0)

    def test_add_new_appointment_success(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        patient = Patient(first_name="John", last_name="Brown")
        patient.save()
        date_time = datetime(2022, 10, 1, tzinfo=timezone.utc)
        appointment_type = "New Patient"

        current_state = Appointment.objects.all().count()
        self.assertEqual(current_state, 0)

        CalendarService.add_new_appointment(doctor.id, patient.id, date_time, appointment_type)

        result = list(Appointment.objects.all().values())
        expected_result = [{'appointment_datetime': date_time,
                            'appointment_type': 'New Patient',
                            'doctor_id': 1,
                            'id': 1,
                            'patient_id': 1}]

        self.assertEqual(result, expected_result)

    def test_add_new_appointment_too_many_appointments(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        patient1 = Patient(first_name="John", last_name="Brown")
        patient1.save()
        patient2 = Patient(first_name="James", last_name="Brown")
        patient2.save()
        patient3 = Patient(first_name="Don", last_name="Brown")
        patient3.save()
        date_time = datetime(2022, 10, 1, tzinfo=timezone.utc)
        appointment_type = "New Patient"

        Appointment(doctor=doctor, patient=patient1, appointment_datetime=date_time,
                    appointment_type=appointment_type).save()
        Appointment(doctor=doctor, patient=patient2, appointment_datetime=date_time,
                    appointment_type=appointment_type).save()
        Appointment(doctor=doctor, patient=patient3, appointment_datetime=date_time,
                    appointment_type=appointment_type).save()

        current_state = Appointment.objects.all().count()
        self.assertEqual(current_state, 3)

        self.assertRaises(Exception, CalendarService.add_new_appointment, doctor.id, patient3.id, date_time,
                          appointment_type)

    def test_add_new_appointment_not_15_min_interval(self):
        doctor = Doctor(first_name='Bob', last_name='Dylan')
        doctor.save()
        patient = Patient(first_name="John", last_name="Brown")
        patient.save()
        date_time = datetime(2022, 10, 1, minute=19, tzinfo=timezone.utc)
        appointment_type = "New Patient"

        self.assertRaises(Exception, CalendarService.add_new_appointment, doctor.id, patient.id, date_time,
                          appointment_type)


class ViewsTestCase(TestCase):
    @patch("app.views.DoctorService.get_doctors", return_value="test_value")
    def test_get_doctors(self, mock_get_doctors: MagicMock):
        resp = self.client.generic("GET", reverse("get_doctors"), content_type='application/json')
        mock_get_doctors.assert_called_once()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,  b'{"doctors_list": "test_value"}')

    @patch("app.views.CalendarService.get_appointments", return_value="test_value")
    def test_get_appointments(self, mock_get_appointments: MagicMock):
        date_time_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        resp = self.client.generic("GET", reverse("get_appointments"), json.dumps({"doctor_id": 2, "appointment_date": date_time_str}), content_type='application/json')
        mock_get_appointments.assert_called_with(2, datetime.strptime(date_time_str, "%m/%d/%Y, %H:%M:%S"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content,  b'{"appointments_list": "test_value"}')

    @patch("app.views.CalendarService.delete_appointment", return_value="test_value")
    def test_delete_appointment(self, mock_delete_appointment: MagicMock):
        resp = self.client.generic("DELETE", reverse("delete_appointment"), json.dumps({"appointment_id": 2}), content_type='application/json')
        mock_delete_appointment.assert_called_with(2)
        self.assertEqual(resp.status_code, 200)

    @patch("app.views.CalendarService.add_new_appointment", return_value="test_value")
    def test_add_new_appointment(self, mock_new_appointment: MagicMock):
        date_time_str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        request_body = {
            "doctor_id": 1,
            "patient_id": 2,
            "appointment_datetime": date_time_str,
            "appointment_type": "New Client"
        }
        resp = self.client.generic("POST", reverse("add_new_appointment"), json.dumps(request_body), content_type='application/json')
        mock_new_appointment.assert_called_with(1, 2, datetime.strptime(date_time_str, "%m/%d/%Y, %H:%M:%S"), "New Client")
        self.assertEqual(resp.status_code, 200)
