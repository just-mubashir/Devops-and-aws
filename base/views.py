from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth import authenticate, logout, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission, Group
from django.contrib import messages
from .models import Post
from base.models import Room, Message
from django.http import HttpResponse, JsonResponse

def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)


@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        post_id = request.POST.get("delete")
        post = Post.objects.filter(id=post_id).first()
        user_to_ban = request.POST.get("ban")
        if post and (request.user.has_perm("main.delete_post") or request.user == post.author):
            post.delete()
        elif user_to_ban and request.user.is_staff:
            user = User.objects.get(username=user_to_ban)
            if user.is_staff:
                messages.error(request, "You cannot ban this user.")
            else:
                group = Group.objects.get(name='default')
                group.user_set.remove(user)
                messages.success(request, "User banned!")

    return render(request, "main/home.html", {"posts": Post.objects.all(), "request": request})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            messages.success(request, "Account Created!")
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "main/sign-up.html", {"form": form})


@login_required(login_url='/login')
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post Created!")
            return redirect("/home")
    else:
        form = PostForm()
    return render(request, "main/create-post.html", {"form": form})

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.uid)
    return JsonResponse({"messages":list(messages.values())})


def chat(request):
    return render(request, 'chat/home.html')