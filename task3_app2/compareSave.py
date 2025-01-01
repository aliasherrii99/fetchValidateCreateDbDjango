from task3_app.models import CreateDb


def show_raw():
    data = CreateDb.objects.raw('SELECT * FROM public."dataBorsDj2"')
    for i in data:
        print(i)
