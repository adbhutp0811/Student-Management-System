from django.views.generic import ListView, DetailView
from .models import Notice


class NoticeListView(ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 20

    def get_queryset(self):
        qs = Notice.objects.filter(is_published=True)
        cat = self.request.GET.get('category')
        if cat:
            qs = qs.filter(category=cat)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Notice.CATEGORY_CHOICES
        ctx['current_category'] = self.request.GET.get('category', '')
        return ctx


class NoticeDetailView(DetailView):
    model = Notice
    template_name = 'notices/notice_detail.html'
    context_object_name = 'notice'
    slug_field = 'pk'
