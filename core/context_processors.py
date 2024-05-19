def inject_request(request):
    """
    Контекстный процессор, который во все шаблоны добавляется
    объект request, чтобы из него можно было получить юзера
    """
    return {'request': request}
