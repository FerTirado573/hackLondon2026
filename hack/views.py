# spaces/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import StudySpace
from django.views.decorators.csrf import csrf_exempt
import json

# spaces/views.py

def home(request):
    # List all study spaces
    spaces = StudySpace.objects.all()
    return render(request, 'hack/index.html', {'spaces': spaces})

def space_detail(request, space_id):
    # Show busy hours for a single space
    space = get_object_or_404(StudySpace, id=space_id)
    
    # For hackathon, we simulate busy hours
    busy_hours = [0,1,1,0,0,1,1,0,0]  # Example: 8AM - 4PM
    labels = ['8AM','9AM','10AM','11AM','12PM','1PM','2PM','3PM','4PM']

    return render(request, 'hack/space_detail.html', {
        'space': space,
        'busy_hours': busy_hours,
        'labels': labels
    })

@csrf_exempt  # for simple hackathon API (not recommended for production)
def update_occupancy(request, space_id):
    """
    Simple API to update the occupied status of a space.
    PIR device sends a POST with JSON: {"occupied": true}
    """
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=400)

    space = get_object_or_404(StudySpace, id=space_id)
    
    try:
        data = json.loads(request.body)
        occupied = data.get('occupied')
        if occupied is None:
            return JsonResponse({"error": "occupied field required"}, status=400)
        
        space.occupied = bool(occupied)
        space.save()
        return JsonResponse({"success": True, "occupied": space.occupied})
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid JSON"}, status=400)
