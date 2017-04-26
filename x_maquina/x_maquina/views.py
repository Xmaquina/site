from django.shortcuts import render

# HTTP Error 400
def bad_request(request):
    return render(request, '400.html', status=400)

# HTTP Error 403
def permission_denied(request):
    return render(request, '403.html', status=403)

# HTTP Error 404
def page_not_found(request):
    return render(request, '404.html', status=404)

# HTTP Error 500
def server_error(request):
    return render(request, '500.html', status=500)
