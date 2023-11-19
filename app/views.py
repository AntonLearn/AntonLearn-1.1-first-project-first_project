import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time_obj = datetime.datetime.now()
    current_time = current_time_obj.strftime("%H:%M:%S")
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    path = '.'
    template_name = 'app/workdir.html'
    messages = dict()
    tree_list = list(os.walk(path))
    tree_list_up_level_dirs = tree_list[0][1]
    len_tree_list_up_level_dirs = len(tree_list_up_level_dirs)
    tree_list_up_level_files = tree_list[0][2]
    len_tree_list_up_level_files = len(tree_list_up_level_files)
    if len(tree_list_up_level_dirs) == 0 and len(tree_list_up_level_files) == 0:
        messages['Пустая рабочая директория!'] = reverse('workdir')
    else:
        messages['Содержимое рабочей директории:'] = reverse('workdir')
        if len_tree_list_up_level_dirs > 0:
            messages['Папки:'] = reverse('workdir')
            for name_dir in tree_list_up_level_dirs:
                messages[f'-- {name_dir}'] = reverse('workdir')
        if len_tree_list_up_level_files > 0:
            messages['Файлы:'] = reverse('workdir')
            for name_file in tree_list_up_level_files:
                messages[f'-- {name_file}'] = reverse('workdir')
    context = {
        'messages': messages
    }
    return render(request, template_name, context)
