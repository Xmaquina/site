from django.shortcuts import render
from request.forms import RequestForm


def request_list(request):
    return render(request, 'request/requests.html', {})


def request_new(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Solicitação recebida!")
            except Exception as e:
                messages.error(request, "Falha ao salvar solicitação!")
                return render(request, 'ue/prospect_form.html', {
                    'prospect_form': prospect_form,
                    'company_form': company_form})
            return redirect('Home')
    else:
        request_form = RequestForm()
        return render(request, 'request/request_form.html', {
                'form': request_form})
