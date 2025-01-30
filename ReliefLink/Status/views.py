# Status/views.py
from django.shortcuts import render, get_object_or_404
from home.models import Division, District, Upazila, Union, Ward
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
            floody_upazilas = json.loads(district.floody_upazilas)
            if floody_upazilas:
                filtered_districts.append(district)
        except json.JSONDecodeError:
            continue
    
    return render(request, 'status/district_status.html', {
        'division' : division,
        'districts': filtered_districts,
    })


def upazila_status(request, district_id):
    district = get_object_or_404(District, id=district_id)
    
    upazilas = Upazila.objects.filter(district=district)

    filtered_upazilas = []
    for upazila in upazilas:
        try:
            floody_unions = json.loads(upazila.floody_unions)
            if floody_unions:
                filtered_upazilas.append(upazila)
        except json.JSONDecodeError:
            continue
    
    return render(request, 'status/upazila_status.html', {
        'district' : district,
        'upazilas': filtered_upazilas,
    })


def union_status(request, upazila_id):
    upazila = get_object_or_404(Upazila, id=upazila_id)
    
    unions = Union.objects.filter(upazila=upazila)

    filtered_unions = []
    for union in unions:
        try:
            floody_wards = json.loads(union.floody_wards)
            if floody_wards:
                filtered_unions.append(union)
        except json.JSONDecodeError:
            continue
    
    return render(request, 'status/union_status.html', {
        'upazila' : upazila,
        'unions': filtered_unions,
    })


def ward_status(request, union_id):
    union = get_object_or_404(Union, id=union_id)
    
    wards = Ward.objects.filter(union=union)

    filtered_wards = []
    for ward in wards:
        try:
            if ward.is_flood:
                filtered_wards.append(ward)
        except json.JSONDecodeError:
            continue
    
    return render(request, 'status/ward_status.html', {
        'union' : union,
        'wards': filtered_wards,
    })