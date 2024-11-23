from django.shortcuts import render
from .forms import ExampleForm
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


# Create your views here.
@permission_required('bookshelf.CustomUser', raise_exception= True)
def SayHello(request):
    book_list = ['']
    return HttpResponse('Hello Worled')
    
