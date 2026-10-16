from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Attendance

user = get_user_model()

def mark_attendance(request):

    if request.user.role != "SUPERWISER":
        return redirect("authenti:login")

    workers = user.objects.filter(role = "WORKER"  , superwiser = request.user)

    if request.method == 'POST':
        date = request.POST['date']

        for worker in workers:
            status = request.POST.get(f"attendance_{worker.id}")

            if status:
                Attendance.objects.update_or_create(worker = worker , date = date ,  defaults = {"status" : status})

        return redirect('attendance:attendance-history')


    return render(request , "mark_attendance.html" , {"workers" : workers})


@login_required
def attendance_history(request):

    if request.user.role != "SUPERWISER":
        return redirect("authenti:login")

    attendance = Attendance.objects.all().order_by("-date" )
    dates = attendance.values_list('date' , flat= True).distinct()

    daily_data = []

    for date in dates:

        records = Attendance.objects.filter(date=date)

        absent = records.filter(status="ABSENT").count()
        present = records.filter(status = "PRESENT").count()

        daily_data.append({
            "date": date,
            "records": records,
            "absent": absent,
            "present" : present,
        })

    return render(request , "attendance_history.html" , {'attendance' : attendance , 'dates': dates ,"daily_data" : daily_data })



@login_required
def worker_attendance(request):
    if request.user.role != "SUPERWISER":
        return redirect("authenti:login")

    attendance = Attendance.objects.filter(worker = request.user).order_by("-date")
    return render(request, "worker_attendance_history.html" , {"attendance": attendance})
