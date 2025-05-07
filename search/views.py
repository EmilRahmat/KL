from django.shortcuts import render

def search_view(request):
    query = request.GET.get("q")
    context = {"query": query}
    return render(request, "search/results.html", context)
