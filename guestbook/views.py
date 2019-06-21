from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import GuestBook


def list(request):
    guestbooklist = GuestBook.objects.all().order_by('-id')
    data = {'guestbooklist': guestbooklist}
    return render(request, 'guestbook/list.html', data)

def deleteform(request, id):
    data = {'id' : id}
    return render(request,'guestbook/deleteform.html', data)
def delete(request):
    id = request.POST['id']
    password = request.POST['password']
    guestbook = GuestBook.objects.filter(id=id).filter(password=password)
    guestbook.delete()
    return HttpResponseRedirect('/guestbook/')

def add(request):
    guestbook = GuestBook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']

    guestbook.save()
    return HttpResponseRedirect('/guestbook/')