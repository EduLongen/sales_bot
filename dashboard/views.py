from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect
from .forms import RegisterForm, EditUserForm, CategoryForm, ProductForm  
from .models import User, Category, Client, Product, PixPayment, Order, OrderItem
from .utils import send_telegram_message

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
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
def edit_product(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit products.")
    
    product = get_object_or_404(Product, pk=id)
    categories = Category.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        print(form.errors)
        print(form.cleaned_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso.")
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/products.html', {
        'form': form, 
        'product': product
    })


@login_required
def add_user(request):
    return render(request, 'dashboard/add_user.html')

@login_required
def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})

@login_required
def clients_list(request):
    clients = Client.objects.filter(is_deleted=False)
    return render(request, 'dashboard/clients.html', {'clients': clients})

@login_required
def delete_client(request, client_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete clients.")
    
    # Recupera o cliente, mesmo que não deletado
    client_to_delete = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        # Marca como deletado em vez de remover o registro
        client_to_delete.is_deleted = True
        client_to_delete.save()
        messages.success(request, "Cliente marcado como deletado com sucesso.")
        return redirect('clients')

    return redirect('clients')

@login_required
def messages_list(request):
    return render(request, 'dashboard/messages.html')

@login_required
def orders_list(request):
    orders = Order.objects.all()
    orders_items = OrderItem.objects.all()
    
    orders_with_items = []
    for order in orders:
        items = orders_items.filter(order_id=order.id)
        orders_with_items.append({
            'order': order,
            'items': items,
        })

    context = {
        'orders_with_items': orders_with_items,
    }
    return render(request, 'dashboard/orders.html', context)

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
def products_list(request):
    products = Product.objects.all()
    categories = Category.objects.filter(is_active=True) 
    return render(request, 'dashboard/products.html', {'products': products, 'categories': categories}) 

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
def transmission(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        if not message:
            messages.error(request, 'A mensagem não pode estar vazia!')
            return render(request, 'dashboard/transmission.html', {'text': message})

        try:
            chat_ids = Client.objects.values_list('chat_id', flat=True)
            if not chat_ids:
                messages.error(request, 'Não há chat_ids registrados no banco de dados.')
                return render(request, 'dashboard/transmission.html', {'text': message})

            errors = send_telegram_message(message, chat_ids)
            if errors:
                messages.error(request, f'Erro ao enviar mensagem: {errors}')
                return render(request, 'dashboard/transmission.html', {'text': message})

            messages.success(request, 'Mensagens enviadas com sucesso!')
            return render(request, 'dashboard/transmission.html', {'text': message})

        except Exception as e:
            messages.error(request, f'Ocorreu um erro inesperado: {str(e)}')
            return render(request, 'dashboard/transmission.html', {'text': message})

    return render(request, 'dashboard/transmission.html')