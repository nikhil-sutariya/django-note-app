from django.shortcuts import redirect, render
from .forms import NoteForm
from .models import Note
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def home(request):
    if request.user.is_superuser:
        notes = Note.objects.all()
    else:
        notes = Note.objects.filter(user=request.user)
    return render(request, 'home.html', {'notes':notes})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home') 
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2: 
            if User.objects.filter(username=username).exists():
                messages.success(request, 'This username is already taken.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.success(request, 'This email is already taken.') 
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                messages.success(request, 'Account created successfully, now login to continue.')
                return redirect('login')
        else:
            messages.success(request, 'Password and confirm password must be same.')
        return redirect('home')
    return render(request, 'signup.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'You are successfully logged out!')
    return redirect('login')

def noteform(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            n = form.save(commit=False)
            n.user = request.user
            n.save()
            messages.success(request, 'Note created successfully.')
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'note-form.html', {'form':form})

def editnote(request,id):
    notes = Note.objects.get(id = id)
    form = NoteForm(request.POST, instance=notes)
    if form.is_valid():
            form.save()
            messages.success(request, 'Note edited successfully.')
            return redirect('home')
    return render(request, 'edit-post.html', {'notes':notes})

def deletenote(request,id):
    notes = Note.objects.get(id = id)
    notes.delete()
    messages.success(request, 'Note deleted successfully.')
    return redirect('home')
