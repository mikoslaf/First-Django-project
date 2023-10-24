from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# lista = [
#     {"id":1, "name":"Pierwszy znak"},
#     {"id":2, "name":"Drugi znak"},
#     {"id":3, "name":"Trzeci znak"},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: # jeśli user jest zalogowany
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exits')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exits')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    context = {'page': page}

    return render(request, 'login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''  # pobieramy zmienna z linku 

    lista = Room.objects.filter(
        Q(topic__name__icontains = q) | # & == and, | == or
        Q(name__icontains = q) |
        Q(description__icontains = q)
        ) # Podczas zapytań do bd zamist . używa się __ chyba | icontains dodajce coś w stylu LIKE "%cos%"

    topic = Topic.objects.all()
    rooms_count = lista.count()

    context =  {'name': 'Start', 'lista': lista, 'topics': topic, 'room_count': rooms_count}
    return render(request, "lista.html", context)

def list(request, pk):
    # val = None
    # for x in lista:
    #     if int(pk) == x["id"]:
    #         val = x["name"]
    #         break
    val = Room.objects.get(id=pk)
    context =  {'id': pk,'value': val}
    return render(request, "list.html", context)

@login_required(login_url='login') # Gdy nie jesteś zalogowany przekierowuje do login/ | To jest dekorator
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST': # Zapisywanie wartości z form
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "list_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # Taki selece z sql
    form = RoomForm(instance=room) # wstaja do inputów dane z wyszukanego wiersza

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "list_form.html", context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) # Taki selece z sql
    form = RoomForm(instance=room) # wstaja do inputów dane z wyszukanego wiersza

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!')
    
    if request.method == 'POST':
        room.delete() # usuwa wiersz z bazdy danych
        return redirect('home')

    context = {'form': form, 'obj': room}
    return render(request, "list_delete.html", context)
