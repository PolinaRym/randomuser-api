from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.core.paginator import Paginator
import random

# Главная страница с формой и таблицей

def user_list(request):
    count = request.GET.get('count', 20)
    try:
        count = int(count)
        if count < 1 or count > 1000:
            count = 20
    except ValueError:
        count = 20
    users = UserProfile.objects.all()[:count]
    paginator = Paginator(users, 20)  # 20 пользователей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/user_list.html', {'page_obj': page_obj, 'count': count})

# Страница пользователя по id

def user_detail(request, uuid):
    user = get_object_or_404(UserProfile, uuid=uuid)
    return render(request, 'users/user_detail.html', {'user': user})

# Страница случайного пользователя

def random_user(request):
    count = UserProfile.objects.count()
    if count == 0:
        return redirect('user_list')
    random_index = random.randint(0, count - 1)
    user = UserProfile.objects.all()[random_index]
    return render(request, 'users/user_detail.html', {'user': user, 'random': True})
