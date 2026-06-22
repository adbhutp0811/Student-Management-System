from django.views.generic import ListView
from .models import FeeStructure, Payment
from django.shortcuts import render


class FeeListView(ListView):
    model = FeeStructure
    template_name = 'fees/fee_list.html'
    context_object_name = 'fee_structures'
