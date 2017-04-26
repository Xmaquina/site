from django.shortcuts import render

def request_list(request):
    return render(request, 'request/requests.html', {})
