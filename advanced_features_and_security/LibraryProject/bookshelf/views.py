from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

# Create your views here.
@permission_required('bookshelf.CustomUser', raise_exception= True)
def SayHello(request):
    book_list = list('')
    return HttpResponse('Hello Worled')
    