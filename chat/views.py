from django.shortcuts import render

from .models import Chat

def room(request, room_name):
    chat = Chat.objects.get(slug=room_name)
    return render(request, 'chatroom.html', {
            'room_name': room_name,
            'initial_data': chat.data,
            'chat': chat,
        })