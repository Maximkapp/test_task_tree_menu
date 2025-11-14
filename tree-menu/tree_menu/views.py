from django.shortcuts import render
from django.db import connection
from tree_menu.templatetags.menu_tags import draw_menu

def test_menu_view(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'projects.html')


def project1(request):
    return render(request, 'project1.html')

def project1_1(request):
    # очищаем список запросов
    connection.queries.clear()

    # отрисовка меню (как в шаблоне)
    context = {'request': request}
    draw_menu(context, 'main_menu')

    # проверка
    print(f"Количество SQL-запросов: {len(connection.queries)}")
    for q in connection.queries:
        print(q['sql'])
    return render(request, 'project1.1.html')