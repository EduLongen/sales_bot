from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegisterForm, EditUserForm, CategoryForm, MessageForm, PixPaymentForm  
from .models import User, Category, Client, Message, PixPayment

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'user': request.user})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('categories')  
    else:
        form = CategoryForm()
    return render(request, 'dashboard/add_category.html', {'form': form})

@login_required
def edit_category(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit categories.")
    
    category = get_object_or_404(Category, pk=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.is_active = form.cleaned_data['is_active']
            category.save()
            messages.success(request, "Categoria atualizada com sucesso.")
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/categories.html', {'form': form, 'category': category})

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
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})

@login_required
def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/clients.html', {'clients': clients})

@login_required
def delete_client(request, client_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete clients.")
    
    client_to_delete = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        client_to_delete.delete()
        messages.success(request, "Cliente deletado com sucesso.")
        return redirect('clients')

    return redirect('clients')

@login_required
def messages_list(request):
    return render(request, 'dashboard/messages.html')

@login_required
def orders_list(request):
    return render(request, 'dashboard/orders.html')

@login_required
def payment_page(request):
    if request.method == 'POST':
        pix_key = request.POST.get('chave')
        description = request.POST.get('description', '')

        if not pix_key:
            messages.error(request, 'Chave PIX é obrigatória.')
            return redirect('payment')

        # Create a new PixPayment object
        pix_payment = PixPayment.objects.create(
            pix_key=pix_key,
            description=description
        )

        # Generate QR code
        pix_payment.generate_qr_code()

        messages.success(request, 'Chave PIX salva e QR Code gerado com sucesso.')
        return redirect('payment')

    # Fetch existing PIX payments for display
    pix_payments = PixPayment.objects.all()
    return render(request, 'dashboard/payment.html', {'pix_payments': pix_payments})

def delete_pix_payment(request, pix_id):
    # Ensure it's a POST request or proper confirmation
    if request.method == "POST":
        pix_payment = get_object_or_404(PixPayment, id=pix_id)
        pix_payment.delete()
        messages.success(request, "Chave PIX excluída com sucesso!")
        return redirect('payment')  # Redirect to payment list page
    else:
        # Return a response or raise a 405 Method Not Allowed
        messages.error(request, "Operação inválida.")
        return redirect('payment')

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
    mensagens2 = Message.objects.all().order_by('-created_at')  # Fetch all messages
    return render(request, 'dashboard/messages.html', {'mensagens2': mensagens2})

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
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    if not request.user.is_superuser and message.user != request.user:
        messages.error(request, "Você não tem permissão para editar esta mensagem.")
        return redirect('messages')
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)  
        if form.is_valid():
            form.save()  # Salva as alterações
            messages.success(request, "Mensagem atualizada com sucesso.")
            return redirect('messages')
    else:
        form = MessageForm(instance=message)  

    return render(request, 'dashboard/edit_message.html', {'form': form, 'message': message})

@login_required
def delete_message(request, message_id):
    message_to_delete = get_object_or_404(Message, id=message_id)
    
    if not request.user.is_superuser and message_to_delete.user != request.user:
        messages.error(request, "Você não tem permissão para excluir esta mensagem.")
        return redirect('messages')  

    if request.method == 'POST':
        message_to_delete.delete()
        messages.success(request, "Mensagem deletada com sucesso.")
        return redirect('messages')
    return redirect('messages')

@login_required
def pix_list_view(request):
    pix_keys = PixPayment.objects.all() 
    return render(request, 'dashboard/payment.html', {'pix_keys': pix_keys})


@login_required
def pix_add_view(request):
    if request.method == 'POST':
        form = PixPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chave Pix adicionada com sucesso!')
            return redirect('payment')  # Redireciona para a lista de chaves Pix
        else:
            messages.error(request, 'Erro ao adicionar a chave Pix. Tente novamente.')
    else:
        form = PixPaymentForm()
    pix_keys = PixPayment.objects.all() 
    return render(request, 'dashboard/payment.html', {'form': form, 'pix_keys': pix_keys})

@login_required
def delete_pix_key(request, pk):
    pix_key = get_object_or_404(PixPayment, pk=pk)
    if request.method == 'POST':
        pix_key.delete()
        messages.success(request, 'Chave Pix deletada com sucesso!')
    return redirect('payment') 