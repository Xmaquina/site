# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib import messages
from request.forms import RequestForm
from request.models import Request
import traceback
import subprocess


def request_list(request):
    reqs = None
    if request.user.is_superuser:
        pending_requests = Request.objects.filter(
            status=Request.RECEIVED).order_by('-sent_at')
        other_requests = Request.objects.exclude(
            status=Request.RECEIVED).order_by('-sent_at')
        total_reqs = Request.objects.count()
        total_concluded_reqs = Request.objects.filter(
            status=Request.SUCCESS).count()
        total_negated_reqs = Request.objects.filter(
            status=Request.CANCELLED).count()
    else:
        try:
            pending_requests = Request.objects.filter(
                owner=request.user, status=Request.RECEIVED).order_by('-sent_at')
            other_requests = Request.objects.filter(
                owner=request.user).exclude(
                status=Request.RECEIVED).order_by('-sent_at')
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
                   'other_requests': other_requests,
                   'total_reqs': total_reqs,
                   'total_concluded_reqs': total_concluded_reqs,
                   'total_negated_reqs': total_negated_reqs})


def request_new(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            try:
                req = request_form.save(commit=False)
                req.owner = request.user
                try:
                    req.save()
                    gcode_process_out = subprocess.check_output(
                        'Slic3r/slic3r.pl ' + str(req.cad_file.path),
                        shell=True, timeout=5)
                    messages.success(request, "Solicitação recebida!")
                    return redirect('Home')
                except subprocess.CalledProcessError as gcode_exception:
                    req.delete()
                    print("error code " + str(gcode_exception.returncode) +
                          str(gcode_exception.output))
                    messages.error(
                        request, "Arquivo STL não pôde ser validado!")
            except Exception as e:
                print(e)
                traceback.print_exc()
            messages.error(request, "Falha ao salvar solicitação!")
    else:
        request_form = RequestForm()
    return render(request, 'request/request_form.html', {
        'form': request_form})
