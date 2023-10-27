from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta: 
        model = Room 
        fields = '__all__' # daje użytkownikowi wszystkie pola
        exclude = ['host', 'participants'] # Wyklucza dane pola