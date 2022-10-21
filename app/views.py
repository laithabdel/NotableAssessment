import json
import sqlite3
from datetime import datetime

from django.http import HttpResponse
from rest_framework.decorators import api_view

from app.services import CalendarService, DoctorService


@api_view(["GET"])
def get_doctors(request):
    try:
        doctors_list = DoctorService.get_doctors()
        return HttpResponse(content=json.dumps({"doctors_list": doctors_list}))
    except (sqlite3.Error, AttributeError, ValueError, json.JSONDecodeError):
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=500)


@api_view(["GET"])
def get_appointments(request):
    try:
        payload = json.loads(request.body)
        doctor_id = payload["doctor_id"]
        appointment_date = datetime.strptime(payload["appointment_date"], "%m/%d/%Y, %H:%M:%S")
        appointments_list = CalendarService.get_appointments(doctor_id, appointment_date)
        return HttpResponse(content=json.dumps({"appointments_list": appointments_list}, default=str))
    except (sqlite3.Error, AttributeError, ValueError, json.JSONDecodeError):
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=500)


@api_view(["DELETE"])
def delete_appointment(request):
    try:
        payload = json.loads(request.body)
        appointment_id = payload["appointment_id"]
        CalendarService.delete_appointment(appointment_id)
        return HttpResponse()
    except (sqlite3.Error, AttributeError, ValueError, json.JSONDecodeError):
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=500)


@api_view(["POST"])
def add_new_appointment(request):
    try:
        payload = json.loads(request.body)
        doctor_id = payload["doctor_id"]
        patient_id = payload["patient_id"]
        appointment_datetime = datetime.strptime(payload["appointment_datetime"], "%m/%d/%Y, %H:%M:%S")
        appointment_type = payload["appointment_type"]
        appointment_id = CalendarService.add_new_appointment(doctor_id, patient_id, appointment_datetime, appointment_type)
        return HttpResponse(content=json.dumps({"appointment_id": appointment_id}))
    except (sqlite3.Error, AttributeError, ValueError, json.JSONDecodeError):
        return HttpResponse(status=400)
    except Exception:
        return HttpResponse(status=500)


