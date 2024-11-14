from django.shortcuts import render, redirect
from .models import Rooms, Messages, Private_rooms, Private_messages, User_Info
from django.contrib import messages
from .forms import MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User



@login_required(login_url='login')
def home(request):
    q = request.GET.get('q', '')  # Default to empty string if 'q' is not provided
    user_info = User_Info.objects.get(user=request.user)
    have_request = False
    if user_info.request_friend.count() != 0:
        have_request = True

    # Filter friends based on search query
    friends = user_info.friends.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(username__icontains=q)
    )

    for friend in friends:
        user_id = user_info.user.id
        friend_id = friend.id

        # Normalize the user order
        user1_id = min(user_id, friend_id)
        user2_id = max(user_id, friend_id)

        # Check if a room already exists for this pair of users
        if not Private_rooms.objects.filter(user_id=user1_id, friend_id=user2_id).exists():
            # If not, create a new room
            Private_rooms.objects.get_or_create(user_id=user1_id, friend_id=user2_id)

    # Filter private rooms based on search query
    private_rooms = Private_rooms.objects.filter(
        Q(user=user_info.user) |
        Q(friend=user_info.user)
    ).filter(
        Q(friend__username__icontains=q) |
        Q(friend__last_name__icontains=q) |
        Q(friend__first_name__icontains=q)
    )

    context = {
        'user_info': user_info,
        'friends': friends,
        'private_rooms': private_rooms,
        'have_request': have_request
    }
    return render(request, 'home.html', context)



def message_room_view(request, pk):
    room = Private_rooms.objects.get(id=pk)
    messages = Private_messages.objects.filter(room=room)
    user_info = User_Info.objects.get(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        room_id = request.POST.get('room_id')
        # print(room_id)
        if message:
            message = message.strip()
            if message:
                Private_messages.objects.create(content=message, room=room, user=request.user)
        elif room_id:
            room_to_delete = Private_rooms.objects.get(id=room_id)
            if room_to_delete.user == request.user:
                if room_to_delete.friend in user_info.friends.all():
                    user_info.friends.remove(room_to_delete.friend)
                    room_to_delete.friend.user_info.friends.remove(request.user)
                    room_to_delete.delete()
                    return redirect('home')
            else:
                if room_to_delete.user in user_info.friends.all():
                    user_info.friends.remove(room_to_delete.user)
                    room_to_delete.user.user_info.friends.remove(request.user)
                    room_to_delete.delete()
                    return redirect('home')
            
    context = {
        'room': room,
        'messages': messages, 
    }
    return render(request, 'message.html', context)



@login_required(login_url='login')
def add_friend(request):
    available = User.objects.exclude(username=request.user.username)
    user_info = request.user.user_info
    current_friends = user_info.friends.all()
    pending_requests = user_info.request_friend.all()
    
    available_friend = available.exclude(id__in=current_friends).exclude(id__in=pending_requests)
    if  request.method == 'POST':
        user_id = request.POST.get('user-id')
        user = User.objects.get(id=user_id)
        user_info = User_Info.objects.get(user=user)
        user_info.request_friend.add(request.user)
    
    context = {
        'available_friends': available_friend,
    }
    return render(request, 'find_friend.html', context)


@login_required(login_url='login')
def requested_friend_view(request):
    user_info = User_Info.objects.get(user=request.user)
    requested_friends = user_info.request_friend.all()
    if request.method == 'POST':
        accept = request.POST.get('accept')
        deny = request.POST.get('deny')
        if accept:
            accept_user= User.objects.get(id=accept)
            user_info.friends.add(accept_user)
            user_info.request_friend.remove(accept_user)
            accept_user.user_info.friends.add(request.user)
            # Private_rooms.objects.get_or_create(user=user_info.user, )
        elif deny:
            deny_user = User.objects.get(id=deny)
            user_info.request_friend.remove(deny_user)
            
         
    context = {
        'requested_friends': requested_friends,
    }
    return render(request, 'requested_friend.html', context)

#Registration

def signup_view(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user_info, created = User_Info.objects.get_or_create(user=user, id=user.id)
            user_info.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Form is invalid')
    
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def login_view(request):
    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)
       if user is not None:
           user_info, created = User_Info.objects.get_or_create(user=user)
           user_info.save()
           login(request, user)
           return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')