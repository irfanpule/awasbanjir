from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings

from perangkat.models import Perangkat
from awasbanjir.mixin import ContextTitleMixin


class PantautListView(ContextTitleMixin, ListView):
    model = Perangkat
    paginate_by = 12
    title_page = 'Daftar Perangkat'
    for_public = True
    template_name = 'perangkat/pantau_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['for_public'] = self.for_public
        return context

    def get_queryset(self):
        return self.model.objects.all()


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


class PantauView(ContextTitleMixin, DetailView):
    model = Perangkat
    template_name = 'perangkat/monitor.html'
    title_page = "Pantau"

    def get_title_page(self):
        return f"Pantau data {self.object.nama}"


class RiwayatView(PantauView):
    template_name = 'perangkat/riwayat.html'
    title_page = "Riwayat"

    def get_title_page(self):
        return f"Riwayat data {self.object.nama}"


@method_decorator(login_required, name='dispatch')
class PerangkatListView(PantautListView):
    for_public = False
    template_name = 'perangkat/perangkat_list.html'

    def get_queryset(self):
        return self.model.objects.filter(pemilik=self.request.user)


class GetDataSeriesView(DetailView):
    model = Perangkat
    slug_field = 'device_id'
    slug_url_kwarg = 'device_id'
    str_date_char_label = "%H:%M:%S"
    start_date = None
    end_date = None
    limit = settings.LIMIT_LIVE_GRAPH
    
    def _struct_response(self):
        return {
            'label_series': [],
            'data_series': [],
            'status': '....',
            'jarak': '....',
            'waktu': '....'
        }

    def get(self, request, *args, **kwargs):
        data_series = self.get_queryset_data_series()
        context = self._struct_response()
        if data_series:
            last_data = data_series.last()
            if self.limit:
                data_series = data_series[100:]
            context = self._struct_response()
            context['label_series'] = [str(data.created_at.strftime(self.str_date_char_label)) for data in data_series]
            context['data_series'] = [data.jarak for data in data_series]
            context['status'] = last_data.get_status_display()
            context['jarak'] = last_data.jarak
            context['waktu'] = str(last_data.created_at.strftime("%M:%S")) 
        return JsonResponse(data=context, status=200)

    def get_queryset_data_series(self):

        return self.get_object().dataseries_set.filter(created_at__date=datetime.now().date())


class GetDataSeriesHistoryView(GetDataSeriesView):
    model = Perangkat
    str_date_char_label = "%d %b %Y, %H:%M:%S"
    limit = None

    def dispatch(self, request, *args, **kwargs):
        start_date_str = self.request.GET.get('start_date', '')
        end_date_str = self.request.GET.get('end_date', '')
        if start_date_str and end_date_str:
            self.start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
            self.end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset_data_series(self):
        return self.get_object().dataseries_set.filter(
            created_at__date__gte=self.start_date, created_at__date__lte=self.end_date)


class GetLastDataView(GetDataSeriesView):
    def get(self, request, *args, **kwargs):
        data_series = self.get_queryset_data_series()
        context = self._struct_response()
        if data_series:
            context['label_series'] = str(data_series.created_at.strftime(self.str_date_char_label))
            context['data_series'] = data_series.jarak
            context['status'] = data_series.get_status_display()
            context['jarak'] = data_series.jarak
            context['waktu'] = str(data_series.created_at.strftime("%M:%S"))
        return JsonResponse(data=context, status=200)

    def get_queryset_data_series(self):
        return self.get_object().dataseries_set.filter(created_at__date=datetime.now().date()).last()


class MonitorIntro(TemplateView):
    template_name = 'perangkat/monitor_intro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_username_channel'] = settings.TELEGRAM_CHANNEL_TARGET
        return context

