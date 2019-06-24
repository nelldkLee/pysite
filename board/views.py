from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max, F
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.apps import Pagination
from board.models import Board
from user.models import User


def list(request):
    pg = __initpage__(request)
    print(pg.start,pg.end)
    boardlist = Board.objects.select_related().order_by('-regdate')[pg.start:pg.end]
    data = {'boardlist': boardlist, 'pg': pg}
    print(request.POST)

    print('check')
    return render(request,'board/list.html',data)
def view(request):
    data = {'pg': __initpage__(request),
            'board':Board.objects.get(id=request.GET['id'])
            }
    print(data['board'].__dict__)
    return render(request,'board/view.html', data)
def modifyform(request):
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    print('check' + str(request.GET['id']))
    print(user)
    board = model_to_dict(Board.objects.filter(id=str(request.GET['id'])).filter(user=str(user['id']))[0])
    print(board)
    data = {'pg': __initpage__(request), 'board': board}

    return render(request,'board/modifyform.html', data)

def modify(request):
    user = request.session.get('authuser')
    board = Board.objects.filter(id=request.POST['id']).filter(user=str(user['id']))[0]
    if board is not None:
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.save()
    return HttpResponseRedirect('/board/view?id='+ request.POST['id'])

def writeform(request):
    data = {'pg': __initpage__(request),
            'groupno': request.GET.get('groupno', Board.objects.aggregate(groupno_max=Max('groupno'))['groupno_max']),
            'orderno': request.GET.get('orderno', 1),
            'depth': request.GET.get('depth', 0)
            }

    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    return render(request,'board/writeform.html', data)

def write(request):
    board = __parameterhandler__(request.POST, Board())
    print('test')
    print(board.id)
    print(board)

    if board.id is not None:
        Board.objects.filter(id=board.id).filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)
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

def __initpage__(request):
    page = int(request.GET.get('page', 1))
    perpagesize = int(request.GET.get('perpagesize', 10))

    value = Board.objects.aggregate(board_count=Count('id'))
    pg = Pagination(page, perpagesize, value['board_count'])
    return pg

def __parameterhandler__(requestmethod, model):
    parameters = requestmethod.items()
    attrdic = model.__dict__.keys()

    for key, value in parameters:
        if key in attrdic:
            model.__setattr__(key, value)

    return model