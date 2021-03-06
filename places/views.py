from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from places.models import Place


def index(request):
    places = Place.objects.all()
    features = []
    for place in places:
        features.append(
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [place.longitude, place.latitude]
                },
                'properties': {
                    'title': place.title,
                    'placeId': place.slug,
                    'detailsUrl': reverse('place_info', kwargs={'place_primary_key': place.pk})
                }
            }
        )

    context = {
        'places_geojson': {
            'type': 'FeatureCollection',
            'features': features
        }
        
    }

    return render(request, 'index.html', context)


def place_info(request, place_primary_key):
    place = get_object_or_404(Place, pk=place_primary_key)
    response = {
        'title': place.title,
        'imgs': [img.image.url for img in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.latitude,
            'lng': place.longitude
        }
    }

    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': True})
