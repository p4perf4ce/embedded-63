from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

__DEBUG_GREETING_MESSAGE = "Hello, welcome to index. {}"

def index(request: HttpRequest):
    return HttpResponse(content=__DEBUG_GREETING_MESSAGE.format(request.body))

class ShelfView(View):
    def get(self, request: HttpRequest):
        pass
