from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def trigger_500_error(request):
    raise Exception("Test 500")
