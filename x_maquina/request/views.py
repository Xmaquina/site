from django.shortcuts import render, redirect
from django.contrib import messages
from request.forms import RequestForm
import traceback


def request_list(request):
    return render(request, 'request/requests.html', {})


def request_new(request):
    if request.method == 'POST':
        request_form = RequestForm(request.POST, request.FILES)
        if request_form.is_valid():
            try:
                req = request_form.save(commit=False)
                req.owner = request.user
                req.save()
                messages.success(request, "Solicitação recebida!")
                return redirect('Home')
            except Exception as e:
                messages.error(request, "Falha ao salvar solicitação!")
                print(e)
                traceback.print_exc()
    else:
        request_form = RequestForm()
    return render(request, 'request/request_form.html', {
            'form': request_form})
