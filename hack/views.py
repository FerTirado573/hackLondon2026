# spaces/views.py
from datetime import datetime, time, timedelta

from django.utils import timezone

from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Booking, StudySpace
from django.views.decorators.csrf import csrf_exempt
import json

# spaces/views.py

def home(request):
    # List all study spaces
    spaces = StudySpace.objects.all()
    return render(request, 'hack/index.html', {'spaces': spaces})

@csrf_exempt
def update_occupancy(request, space_id):
    if request.method == "POST":
        space = StudySpace.objects.get(id=space_id)
        data = json.loads(request.body)

        occupied = bool(data.get("occupied"))

        space.occupied = occupied

        # 🔥 track motion timestamp
        if occupied:
            space.last_motion_at = timezone.now()

        space.save()

        return JsonResponse({"status": "ok"})
    

# spaces/views.py

def space_detail(request, space_id):
    space = get_object_or_404(StudySpace, id=space_id)

    # Release inactive occupancy
    space.release_if_inactive()

    now = timezone.localtime(timezone.now())  # offset-aware current time

    days = []

    for day_offset in range(7):
        day_date = now.date() + timedelta(days=day_offset)

        # Make aware datetime objects for the start and end of the day
        day_start_naive = datetime.combine(day_date, time(hour=0, minute=0))
        day_start = timezone.make_aware(day_start_naive, timezone.get_current_timezone())

        day_end = day_start + timedelta(days=1)

        # Fetch bookings for this day
        bookings = Booking.objects.filter(
            space=space,
            active=True,
            start_time__gte=day_start,
            start_time__lt=day_end
        )

        booked_hours = set(b.start_time.hour for b in bookings)

        # Hours for the day, e.g., 8am → 21pm
        hours = list(range(8, 22))

        days.append({
            "date": day_date,
            "hours": hours,
            "booked_hours": booked_hours,
        })

    context = {
        "space": space,
        "days": days,
    }

    return render(request, "hack/space_detail.html", context)


def book_space(request, space_id):
    space = get_object_or_404(StudySpace, id=space_id)

    if request.method == "POST":
        start_time_str = request.POST.get("start_time")
        if not start_time_str:
            return redirect(f"/book/{space.id}/?error=1")

        naive_dt = datetime.fromisoformat(start_time_str)
        start_time = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        end_time = start_time + timedelta(hours=1)

        now = timezone.localtime(timezone.now())
        max_booking = now + timedelta(days=7)

        if start_time < now or start_time > max_booking:
            return redirect(f"/book/{space.id}/?error=2")

        overlap = Booking.objects.filter(
            space=space,
            active=True,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlap:
            return redirect(f"/book/{space.id}/?error=3")

        Booking.objects.create(space=space, start_time=start_time, end_time=end_time)
        return redirect("space_detail", space_id=space.id)

    # GET → show form
    now_local = timezone.localtime(timezone.now())
    start_str = request.GET.get("start")
    if start_str:
        try:
            naive_dt = datetime.fromisoformat(start_str)
            pref_dt = timezone.make_aware(naive_dt, timezone.get_current_timezone())
        except ValueError:
            pref_dt = now_local
    else:
        pref_dt = now_local

    pref_start = pref_dt.strftime("%Y-%m-%dT%H:%M")

    context = {
        "space": space,
        "pref_start": pref_start,
        "error": request.GET.get("error")
    }
    return render(request, "hack/book_space.html", context)


