from django.http import HttpResponseRedirect


def home_page(request):
    return HttpResponseRedirect("index.html")
