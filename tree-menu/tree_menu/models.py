from django.db import models

class Menu(models.Model):
    """Модель для представления меню в системе """
    name = models.CharField(max_length=100, unique=True, help_text="Уникальное системное имя меню, например 'main_menu'")
    title = models.CharField(max_length=200, blank=True, help_text="Удобное название для редактирования меню")

    def __str__(self):
        return self.title or self.name

class MenuItem(models.Model):
    """ Модель для представления пунктов меню """
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    named_url = models.CharField(max_length=200, blank=True, help_text="Имя без аргументов")
    url = models.CharField(max_length=500, blank=True, help_text="Прямой URL (пример: /about/ или https://...)")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.IntegerField(default=0, help_text='Порядок среди соседей')

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
