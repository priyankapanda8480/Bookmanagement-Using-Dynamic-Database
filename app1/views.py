from django.shortcuts import render, redirect
from .models import BookData
from django.conf import settings
from django.db import connections
from django.http import HttpResponse

# def switch_db_view(request):
#     if request.GET['use_dynamic_db'] == "true":
#         print(request.GET['use_dynamic_db'])
#         # request.use_dynamic_db = True
#         data = BookData.objects.all()
#         return render(request,'mainpage.html', {'data':data})
#
#     else:
#         # request.use_dynamic_db = False
#         data = BookData.objects.all()
#         return render(request,'mainpage.html', {'data':data})
    # return HttpResponse('Database switch checked.')
default_database = settings.DATABASES['default']

def switch_db_view(request):
    use_dynamic_db = request.GET.get('use_dynamic_db', False) == 'true'
    connections.close_all()
    # print(use_dynamic_db)

    if use_dynamic_db:
        # Set the database connection to the desired dynamic database\

        connections.databases['default'] = settings.DATABASES['dynamic_db']
        return HttpResponse('Dynamically Switched to sqlite3  successfully.')
    else:
        # print(default_database,"success")
        # connections.close_all()
        connections.databases['default'] = settings.DATABASES['default']
        print(connections.databases['default'])
        return HttpResponse('Dynamically Switched to mysql  successfully.')

        # queryset = BookData.objects.using('default').all()
        # return render(request,'mainpage.html', {'data':queryset})
    # else:
    #     # connections.databases['default'] = settings.DATABASES['default']
    #     queryset = BookData.objects.using('dynamic_db').all()
    #     return render(request,'mainpage.html', {'data':queryset})


def mainpage(request):
    data = BookData.objects.all()
    return render(request,'mainpage.html', {'data':data})
# Create your views here.
def addBooks(request):
    return render(request,'addBooks.html')
def addBooks(request):
    if request.method == 'GET':
        return render(request, 'addBooks.html')
    else:
        BookData(
        book_name = request.POST.get('bname'),
        author_name = request.POST.get('authname'),
        book_id =request.POST.get('bookid'),
        book_price =request.POST.get('bookprice')
        ).save()
        return redirect('mainpage')
def update(request, id):
    data = BookData.objects.get(id=id)
    return render(request,'update.html',{'data':data})

def update_data(request,id):
    data = BookData.objects.get(id=id)
    data.book_name=request.POST.get('bname')
    data.author_name=request.POST.get('authname')
    data.book_id=request.POST.get('bookid')
    data.book_price=request.POST.get('bookprice')
    data.save()
    return redirect('mainpage')
def delete(request, id):
    data = BookData.objects.get(id=id)
    data.delete()
    return redirect('mainpage')
