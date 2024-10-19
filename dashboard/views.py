from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

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
    return render(request, 'dashboard/users.html')
