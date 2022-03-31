from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
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
    fields = ['nama', 'tipe', 'lokasi', 'batas_waspada', 'batas_siaga', 'batas_awas', 'beep_alert']
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
    fields = ['nama', 'tipe', 'lokasi', 'batas_waspada', 'batas_siaga', 'batas_awas', 'beep_alert']
    title_page = "Edit Data Perangkat"

    def dispatch(self, request, *args, **kwargs):
        perangkat = self.get_object()
        if perangkat.pemilik != request.user:
            messages.warning(request, f"Anda tidak punya hak untuk mengubah data {perangkat.nama}")
            return redirect("perangkat:list")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = super().post(request, *args, **kwargs)
        messages.success(request, "Berhasil ubah data perangkat")
        return post

    def get_success_url(self):
        return reverse("perangkat:list")


@method_decorator(login_required, name='dispatch')
class PantauView(ContextTitleMixin, DetailView):
    model = Perangkat
    template_name = 'perangkat/monitor.html'
    title_page = "Pantau"

    def get_title_page(self):
        return f"Pantau data {self.object.nama}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_series = self.object.dataseries_set.filter(created_at__date=datetime.now().date())
        context['label_series'] = [str(data.created_at.strftime("%M:%S")) for data in data_series]
        print(context['label_series'])
        context['jarak_series'] = [data.jarak for data in data_series]
        return context


def get_data_series(request, device_id):
    perangkat = get_object_or_404(Perangkat, device_id=device_id)
    data_series = perangkat.dataseries_set.filter(created_at__date=datetime.now().date())
    context = {
        'label_series': [str(data.created_at.strftime("%M:%S")) for data in data_series],
        'data_series': [data.jarak for data in data_series]
    }
    return JsonResponse(data=context, status=200)


def get_last_data(request, device_id):
    perangkat = get_object_or_404(Perangkat, device_id=device_id)
    data = perangkat.dataseries_set.filter(created_at__date=datetime.now().date()).last()
    context = {
        'label_series': str(data.created_at.strftime("%M:%S")),
        'data_series': data.jarak
    }
    return JsonResponse(data=context, status=200)

