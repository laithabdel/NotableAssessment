from datetime import datetime
from app.models import Appointment, Doctor, Patient


class DoctorService:
    @staticmethod
    def get_doctors():
        doctors = Doctor.objects.all().values()
        return list(doctors)

class CalendarService:
    @staticmethod
    def get_appointments(doctor_id: int, appointment_date: datetime):
        doctor = Doctor.objects.get(id=doctor_id)
        appointment_datetime = datetime(appointment_date.year, appointment_date.month, appointment_date.day)
        appointments = Appointment.objects.filter(doctor=doctor, appointment_datetime=appointment_datetime).values()
        return list(appointments)
    
    @staticmethod
    def delete_appointment(appointment_id: int):
        Appointment.objects.get(id=appointment_id).delete()
    
    @staticmethod
    def add_new_appointment(doctor_id: int, patient_id: int, appointment_datetime: datetime, appointment_type: str):
        minutes = appointment_datetime.time().minute
        print(minutes)
        if int(minutes) % 15:
            raise Exception
        doctor = Doctor.objects.get(id=doctor_id)
        num_existing_appointments = Appointment.objects.filter(doctor=doctor, appointment_datetime=appointment_datetime).count()
        if num_existing_appointments >= 3:
            raise Exception
        patient = Patient.objects.get(id=patient_id)
        appointment = Appointment(doctor=doctor,
                                  patient=patient,
                                  appointment_datetime=appointment_datetime,
                                  appointment_type=appointment_type)
        appointment.save()
        return appointment.id


