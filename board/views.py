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
    boardlist = Board.objects.select_related().order_by('-groupno', '-orderno')[pg.start:pg.end]
    data = {'boardlist': boardlist, 'pg': pg}
    print(request.POST)

    print('check')
    return render(request,'board/list.html', data)
def view(request):
    data = {'pg': __initpage__(request),
            'board': Board.objects.get(board_id=request.GET['board_id'])
            }
    print(data['board'].__dict__)
    return render(request, 'board/view.html', data)
def modifyform(request):
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    print('check' + str(request.GET['board_id']))
    print(user)
    board = model_to_dict(Board.objects.filter(board_id=str(request.GET['board_id'])).filter(user=str(user['id']))[0])
    print(board)
    data = {'pg': __initpage__(request), 'board': board}

    return render(request,'board/modifyform.html', data)

def modify(request):
    user = request.session.get('authuser')
    board = Board.objects.filter(board_id=request.POST['board_id']).filter(user=str(user['id']))[0]
    if board is not None:
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.save()
    return HttpResponseRedirect('/board/view?board_id=' + request.POST['board_id'])

def writeform(request):

    # 로그인 여부
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')

    # 요청시 board_id 여부에 따라 게시글과 답글로 분기된다
    groupno_max = Board.objects.aggregate(groupno_max=Max('groupno'))['groupno_max']
    board_id = request.GET.get('board_id', None)
    # 게시글 작성
    if board_id is None:
        print('게시글')
        groupno = 1 if groupno_max is None else groupno_max + 1
        orderno = 1
        depth = 0
    # 답글 작성
    else:
        print('답글')
        board = Board.objects.get(board_id=board_id)
        groupno = board.groupno
        orderno = board.orderno
        depth = board.depth
    data = {'pg': __initpage__(request),
            'board_id': board_id,
            'groupno': groupno,
            'orderno': orderno,
            'depth': depth
    }
    return render(request, 'board/writeform.html', data)

def write(request):

    board = __parameterhandler__(request.POST, Board())
    # input hidden에 value에 값이 없을 때 str타입의 None이 넘어와서 NoneType의 None과 비교 불가하였음.
    if board.board_id is not None:
        Board.objects.filter(board_id=board.board_id).filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)
        board.depth = 1 + int(board.depth)
    board.board_id = None
    board.save()
    return HttpResponseRedirect('/')

def delete(request):
    user = request.session.get('authuser')
    if user is None:
        return HttpResponseRedirect('/user/loginform')
    board = Board.objects.filter(board_id=request.GET['board_id']).filter(user=user['id'])[0]
    if board is not None:
        board.delete()
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

    value = Board.objects.aggregate(board_count=Count('board_id'))
    pg = Pagination(page, perpagesize, value['board_count'])
    return pg

def __parameterhandler__(requestmethod, model):
    parameters = requestmethod.items()
    attrdic = model.__dict__.keys()

    for key, value in parameters:
        if key in attrdic:
            if value != 'None':
                model.__setattr__(key, value)
    return model