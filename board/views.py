from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.apps import Pagination
from board.models import Board
from user.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def list(request):
    page = int(request.GET.get('page', 1))
    perpagesize = int(request.GET.get('perpagesize', 10))
    value = Board.objects.aggregate(board_count=Count('id'))
    print(page,perpagesize)
    pg = Pagination(page,perpagesize,value['board_count'])
    print(pg.start,pg.end)
    boardlist = Board.objects.select_related().order_by('-regdate')[pg.start:pg.end]
    data = {'boardlist': boardlist, 'pg': pg}

    return render(request,'board/list.html',data)
def view(request):
    return render(request,'board/view.html')
def modifyform(request):
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    return render(request,'board/modifyform.html')
def modify(request):
    no = 0
    return HttpResponseRedirect('/board/view?no='+no)
def writeform(request):
    print('check')
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    return render(request,'board/writeform.html')
def write(request):
    board = Board()
    board.title = request.POST['title']
    board.content = request.POST['content']
    board.user = User.objects.get(id=request.POST['user_id'])

    board.save()
    return HttpResponseRedirect('/')

def writetest(request):

    for idx in range(999):
        board = Board()
        board.title = '테스트 제목' + str(idx)
        board.content = '테스트 내용' + str(idx)
        board.user = User.objects.get(id=1)

        board.save()
    return HttpResponseRedirect('/')
