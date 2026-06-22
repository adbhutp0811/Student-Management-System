from django.views.generic import ListView, DetailView
from .models import Hostel, Room


class HostelListView(ListView):
    model = Hostel
    template_name = 'hostel/hostel_list.html'
    context_object_name = 'hostels'


class HostelDetailView(DetailView):
    model = Hostel
    template_name = 'hostel/hostel_detail.html'
    context_object_name = 'hostel'
    slug_field = 'pk'
