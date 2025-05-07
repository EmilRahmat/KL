from django.shortcuts import render

def favorites_view(request):
    return render(request, "favorites/list.html")