from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# lista = [
#     {"id":1, "name":"Pierwszy znak"},
#     {"id":2, "name":"Drugi znak"},
#     {"id":3, "name":"Trzeci znak"},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''  # pobieramy zmienna z linku 
    
    lista = Room.objects.filter(topic__name__icontains = q) # Podczas zapytań do bd zamist . używa się __ chyba | icontains dodajce coś w stylu LIKE "%cos%"

    topic = Topic.objects.all()

    context =  {'name': 'Start', 'lista': lista, 'topics': topic}
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

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST': # Zapisywanie wartości z form
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "list_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # Taki selece z sql
    form = RoomForm(instance=room) # wstaja do inputów dane z wyszukanego wiersza

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, "list_form.html", context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk) # Taki selece z sql
    form = RoomForm(instance=room) # wstaja do inputów dane z wyszukanego wiersza

    if request.method == 'POST':
        room.delete() # usuwa wiersz z bazdy danych
        return redirect('home')

    context = {'form': form, 'obj': room}
    return render(request, "list_delete.html", context)
