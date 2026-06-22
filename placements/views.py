from django.views.generic import ListView, DetailView
from .models import Company, PlacementDrive


class CompanyListView(ListView):
    model = Company
    template_name = 'placements/company_list.html'
    context_object_name = 'companies'


class PlacementDriveListView(ListView):
    model = PlacementDrive
    template_name = 'placements/drive_list.html'
    context_object_name = 'drives'

    def get_queryset(self):
        return PlacementDrive.objects.filter(is_active=True)


class PlacementDriveDetailView(DetailView):
    model = PlacementDrive
    template_name = 'placements/drive_detail.html'
    context_object_name = 'drive'
    slug_field = 'pk'
