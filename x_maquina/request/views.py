# -*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import periodic_task
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseRedirect
from request.forms import RequestForm
from request.models import Request
from request.read_mail import *
import traceback
import subprocess
import os
import os.path


def update_status():
    print("Lendo emails")
    mails = read_mails(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    for k in mails.keys():
        m = k.split(" / ")
        try:
            req = Request.objects.get(pk=m[0])
            req.status = m[1]
            req.save()
        except:
            print("ERRO ATUALIZANDO SOLICITAÇÃO")


@login_required
def request_list(request):
    update_status()
    reqs = None
    if request.user.is_superuser:
        pending_requests = Request.objects.filter(
            status=Request.RECEIVED).order_by('-sent_at')
        ongoing_requests = Request.objects.filter(
            status=Request.IN_PROGRESS).order_by('-sent_at')
        other_requests = Request.objects.exclude(
            status__in=[Request.RECEIVED, Request.IN_PROGRESS]).order_by('-sent_at')
        total_reqs = Request.objects.count()
        total_concluded_reqs = Request.objects.filter(
            status=Request.SUCCESS).count()
        total_negated_reqs = Request.objects.filter(
            status=Request.CANCELLED).count()
    else:
        try:
            pending_requests = Request.objects.filter(
                owner=request.user, status=Request.RECEIVED).order_by('-sent_at')
            ongoing_requests = Request.objects.filter(
                owner=request.user, status=Request.IN_PROGRESS).order_by('-sent_at')
            other_requests = Request.objects.filter(
                owner=request.user).exclude(
                status__in=[Request.RECEIVED, Request.IN_PROGRESS]).order_by('-sent_at')
            total_reqs = Request.objects.filter(owner=request.user).count()
            total_concluded_reqs = Request.objects.filter(
                owner=request.user, status=Request.SUCCESS).count()
            total_negated_reqs = Request.objects.filter(
                owner=request.user, status=Request.CANCELLED).count()
        except BaseException:
            raise PermissionDenied
    return render(request,
                  'request/requests.html',
                  {'pending_requests': pending_requests,
                   'ongoing_requests': ongoing_requests,
                   'other_requests': other_requests,
                   'total_reqs': total_reqs,
                   'total_concluded_reqs': total_concluded_reqs,
                   'total_negated_reqs': total_negated_reqs})


@login_required
def request_new(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            req = request_form.save(commit=False)
            req.owner = request.user
            success = False
            try:
                req.save()
                ext = ".ngc"
                path_g_code = os.path.splitext(req.cad_file.path)[0] + ext
                cmd = "python2 /home/allan/xmaquinaproject/xmaquina/site/x_maquina/pycam/pycam --export-gcode=" \
                      + path_g_code + " " \
                      "--bounds-type=relative-margin " \
                      "--bounds-lower=0.1,0.05,-0.1 " \
                      "--tool-shape=cylindrical " \
                      "--process-milling-style=conventional " \
                      "--tool-spindle-speed=1000 " \
                      "--process-path-strategy=engrave " \
                      "--process-step-down=3.00 " + str(req.cad_file.path)
                try:
                    gcode_process_out = subprocess.check_output(
                        cmd, shell=True, timeout=5)
                    req.g_code.name = path_g_code.split(
                        settings.MEDIA_ROOT)[-1]
                    req.save()
                    if not os.path.exists(path_g_code):
                        # Failed to generate G-code
                        msg = "Falha na geração do G-code, "\
                            "o arquivo não pôde ser convertido! "\
                            "Envie somente modelos 2D nos formatos .dxf ou .stl "\
                            "A solicitação não pôde ser salva."
                        messages.error(request, msg)
                    else:
                        messages.success(request, "Solicitação recebida!")
                        success = True
                except Exception as gcode_exception:
                    print("error code " + str(gcode_exception))
                    messages.error(request, "Erro na geração do G-code!")
            except Exception as operational_error:
                print(operational_error)
                traceback.print_exc()
                messages.error(request, "Falha ao salvar solicitação!")
            if not success:
                try:
                    req.cad_file.delete()
                except:
                    pass
                req.delete()
            return redirect('request:Request_list')
    else:
        request_form = RequestForm()
    return render(request, 'request/request_form.html', {
        'form': request_form})


@login_required
def request_cancel(request, req_id):
    req = get_object_or_404(Request, pk=req_id)
    if not request.user.is_superuser and req.owner != request.user:
        raise PermissionDenied
    if not req.is_available_for_cancelling():
        # Cancelling is not available for other status
        raise ValidationError
    req.status = Request.CANCELLED
    req.save()
    messages.success(request, "Solicitação cancelada!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def request_approve(request, req_id):
    req = get_object_or_404(Request, pk=req_id)
    if not request.user.is_superuser and req.owner != request.user:
        raise PermissionDenied
    success = False
    try:
        success = req.approve()
    except Exception as e:
        print(e)
    if success:
        messages.success(request, "Solicitação aprovada!")
    else:
        messages.error(request, "Falha ao aprovar solicitação!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
