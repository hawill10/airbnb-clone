from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
from django_countries import countries
from . import models, forms


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404


class RoomDetail(DetailView):
    """RoomDetail Definition"""

    model = models.Room


# def search(request):
#     city = request.GET.get("city", "Anywhere")
#     city = str.capitalize(city)
#     country = request.GET.get("country", "KR")
#     room_type = int(request.GET.get("room_type", 0))
#     price = int(request.GET.get("price", 0) or 0)
#     guests = int(request.GET.get("guests", 0) or 0)
#     beds = int(request.GET.get("beds", 0) or 0)
#     bedrooms = int(request.GET.get("bedrooms", 0) or 0)
#     baths = int(request.GET.get("baths", 0) or 0)
#     instant = bool(request.GET.get("instant", False))
#     superhost = bool(request.GET.get("superhost", False))
#     s_amenities = request.GET.getlist("amenities")
#     s_facilities = request.GET.getlist("facilities")

#     form = {
#         "city": city,
#         "s_country": country,
#         "s_room_type": room_type,
#         "price": price,
#         "guests": guests,
#         "beds": beds,
#         "bedrooms": bedrooms,
#         "baths": baths,
#         "instant": instant,
#         "superhost": superhost,
#         "s_amenities": s_amenities,
#         "s_facilities": s_facilities,
#     }

#     room_types = models.RoomType.objects.all()
#     amenities = models.Amenity.objects.all()
#     facilities = models.Facility.objects.all()

#     choices = {
#         "countries": countries,
#         "room_types": room_types,
#         "amenities": amenities,
#         "facilities": facilities,
#     }

#     filter_args = {}

# if city != "Anywhere":
#     filter_args["city__startswith"] = city

# filter_args["country"] = country

# if room_type is not None:
#     filter_args["room_type__pk__exact"] = room_type

# if price is not None:
#     filter_args["price__lte"] = price

# if guests is not None:
#     filter_args["guests__gte"] = guests

# if bedrooms is not None:
#     filter_args["bedrooms__gte"] = bedrooms

# if beds is not None:
#     filter_args["beds__gte"] = beds

# if baths is not None:
#     filter_args["baths__gte"] = baths

# print(instant, superhost)
# if instant is True:
#     filter_args["instant_book"] = True

# if superhost is True:
#     filter_args["host__superhost"] = True

# if len(s_amenities) > 0:
#     for s_amenity in s_amenities:
#         filter_args["amenities__pk"] = int(s_amenity)

# if len(s_facilities) > 0:
#     for s_facility in s_facilities:
#         filter_args["facilities__pk"] = int(s_facility)

# rooms = models.Room.objects.filter(**filter_args)

#     return render(
#         request,
#         "rooms/search.html",
#         {**form, **choices, "rooms": rooms},
#     )


def search(request):

    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            beds = form.cleaned_data.get("beds")
            baths = form.cleaned_data.get("baths")
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if beds is not None:
                filter_args["beds__gte"] = beds

            if baths is not None:
                filter_args["baths__gte"] = baths

            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True

            for amenity in amenities:
                filter_args["amenities"] = amenity

            for facility in facilities:
                filter_args["facilities"] = facility

            qs = models.Room.objects.filter(**filter_args).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            rooms = paginator.get_page(page)

            return render(request, "rooms/search.html", {"form": form, "rooms": rooms})

    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", {"form": form})
