from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from perangkat.models import Perangkat
from awasbanjir.mixin import ContextTitleMixin


@method_decorator(login_required, name='dispatch')
class PerangkatListView(ContextTitleMixin, ListView):
    model = Perangkat
    paginate_by = 12
    title_page = 'Daftar Perangkat'


@method_decorator(login_required, name='dispatch')
class PerangkatCrateView(ContextTitleMixin, CreateView):
    model = Perangkat
    template_name = 'website/form.html'
    fields = ['nama', 'tipe', 'lokasi', 'batas_waspada', 'batas_siaga', 'batas_awas']
    title_page = "Tambah Data Perangkat"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            perangkat = form.save()
            perangkat.pemilik = request.user
            perangkat.save()
            messages.success(request, "Berhasil tambah data perangkat")
            return self.form_valid(form)
        else:
            messages.error(self.request, 'Terjadi masalah, cek kembali isian pada form.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("perangkat:list")


@method_decorator(login_required, name='dispatch')
class PerangkatUpdateView(ContextTitleMixin, UpdateView):
    model = Perangkat
    template_name = 'website/form.html'
    fields = '__all__'
    title_page = "Edit Data Perangkat"

    def post(self, request, *args, **kwargs):
        post = super().post(request, *args, **kwargs)
        messages.success(request, "Berhasil ubah data perangkat")
        return post

    def get_success_url(self):
        return reverse("perangkat:list")
