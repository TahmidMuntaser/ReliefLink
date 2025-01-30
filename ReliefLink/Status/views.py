# Status/views.py
from django.shortcuts import render, get_object_or_404
from home.models import Division, District
import json

def status(request):
    floody_divisions = Division.objects.exclude(floody_districts='[]')
    return render(request, 'status/status.html', {'floody_divisions': floody_divisions})


def district_status(request, division_id):
    division = get_object_or_404(Division, id=division_id)
    
    districts = District.objects.filter(division=division)

    filtered_districts = []
    for district in districts:
        try:
            floody_unions = json.loads(district.floody_upazilas)
            if floody_unions:
                filtered_districts.append(district)
        except json.JSONDecodeError:
            continue
    
    return render(request, 'status/district_status.html', {
        'division' : division,
        'districts': filtered_districts,
    })