from math import ceil

from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = 'board'

class Pagination:

    def __init__(self, page, perpagesize, totalcount):
        showpagesize = 5
        self.page = page
        self.perpagesize = perpagesize
        self.start = (self.page -1) * perpagesize
        self.end = self.start + perpagesize
        self.endpage = ceil(page / showpagesize) * showpagesize
        self.startpage = 1 if page // showpagesize is 0 else self.endpage - showpagesize + 1
        if self.endpage * perpagesize > totalcount:
            self.endpage = ceil(totalcount / perpagesize)
        self.prev = False if self.startpage is 1 else True
        self.next = False if self.endpage * perpagesize <= totalcount else True
        self.range = range(self.startpage, self.endpage + 1)
        self.seturl()
    def prev(self):
        return self.prev

    def next(self):
        return self.next
    def start(self):
        return self.start
    def end(self):
        return self.start
    def prevpage(self):
        return self.startpage - 1
    def nextpage(self):
        return self.endpage + 1

    def seturl(self):
        self.url = ("?page=" + str(self.page) + "&perpagesize=" + str(self.perpagesize))
        print(self.url)

if __name__ == '__main__':
    pagenation = Pagination(6,10,999)
    print(pagenation.startpage)
    print(pagenation.endpage)
    print(pagenation.next)
