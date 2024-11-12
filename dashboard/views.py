from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegisterForm
from .forms import EditUserForm
from .models import User
from .forms import MessageForm
from .models import Message

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'user': request.user})

@login_required
def add_category(request):
    return render(request, 'dashboard/add_category.html')

@login_required
def add_message(request):
    return render(request, 'dashboard/add_message.html')

@login_required
def add_product(request):
    return render(request, 'dashboard/add_product.html')

@login_required
def add_user(request):
    return render(request, 'dashboard/add_user.html')

@login_required
def categories_list(request):
    return render(request, 'dashboard/categories.html')

@login_required
def clients_list(request):
    return render(request, 'dashboard/clients.html')

@login_required
def messages_list(request):
    return render(request, 'dashboard/messages.html')

@login_required
def orders_list(request):
    return render(request, 'dashboard/orders.html')

@login_required
def payment_page(request):
    return render(request, 'dashboard/payment.html')

@login_required
def products(request):
    return render(request, 'dashboard/products.html')

@login_required
def transmission(request):
    return render(request, 'dashboard/transmission.html')

@login_required
def users_list(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'dashboard/users.html', {'users': users})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'dashboard/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_superuser:
                messages.success(request, 'Conta de super usuário criada com sucesso.')
            else:
                messages.success(request, 'Conta de usuário criada com sucesso.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'dashboard/register.html', {'form': form})

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit other users.")
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('users')
    else:
        form = EditUserForm(instance=user)
    
    return render(request, 'dashboard/edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete users.")
    
    user_to_delete = get_object_or_404(User, id=user_id)

    if user_to_delete.is_superuser:
        messages.error(request, "Super usuário não pode ser excluído. 😱")
        return redirect('users')

    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('users')

    return redirect('users')

@login_required
def messages_list(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'dashboard/messages.html', {'messages': messages})

@login_required
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.admin = request.user
            message.save()
            messages.success(request, 'Mensagem adicionada com sucesso!')
            return redirect('messages') 
        else:
            messages.error(request, 'Erro ao adicionar a mensagem. Tente novamente.')
    else:
        form = MessageForm()

    return render(request, 'dashboard/add_message.html', {'form': form})

@login_required
def delete_message(request, message_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Você não tem permissão para deletar mensagens.")

    message_to_delete = get_object_or_404(Message, id=message_id)

    if message_to_delete.admin == request.user:
        messages.error(request, "Você não pode excluir sua própria mensagem.")
        return redirect('messages')  

    if request.method == 'POST':
        message_to_delete.delete()
        messages.success(request, "Mensagem deletada com sucesso.")
        return redirect('messages')

    return render(request, 'dashboard/confirm_delete_message.html', {'message': message_to_delete})