from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
import faker, json
from django.middleware.csrf import get_token

# Create your views here.

def members(request):
    return HttpResponse("Hello world!")

# def create_id() :
#     ids = [fake.ssn() for _ in range(10)]
#     return " ".join(ids)

# @require_http_methods(["GET", "POST"])
# def id(request):
#     num = request.POST.get("num")
#     print(num)
#     if num == "" or num is None:
#         data1 = create_id(5)
#     else:
#         data1 = create_id(num)
#     return HttpResponse(data1)

# def create_name(num):
#     names = [fake.name() for i in range(int(num))] 
#     return " ".join(names)

# def name(request):
#     num = request.GET.get("num")
#     print(num)
#     if num == "" or num is None:
#         data = create_name(20)
#     else:
#         data = create_name(num)
#     return HttpResponse(data)