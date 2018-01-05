from django.db import models


#  todo разнести по разным файликам
# Create your models here.


class Location(models.Model):
    '''id достропримечательности (устанавливается тестирующей системой)'''  # todo 32р беззн число
    id = models.PositiveIntegerField(primary_key=True)
    '''описание достопримечательности (длина не ограничена)'''
    place = models.TextField()
    '''название страны расположения (50 символов максимум)'''
    country = models.CharField(max_length=50)
    '''название города (50 символов максимум)'''
    city = models.CharField(max_length=50)
    '''дистанция от города по прямой в километрах'''  # todo 32р беззн число
    distance = models.PositiveSmallIntegerField()


"""Класс, отвечающий за пользователя. 
Он может посетить много мест, быть в одном и том же в разное время с разными оценками"""


class User(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )

    '''id человека (устанавливается тестирующей системой)'''  # todo 32р беззн число
    id = models.PositiveIntegerField(primary_key=True)
    '''электронная почта (100 символов максимум)'''
    email = models.EmailField(verbose_name="электронная почта")  # todo email also unique
    '''имя (50 символов максимум)'''
    first_name = models.CharField(max_length=50, verbose_name="имя")
    '''фамилия (50 символов максимум)'''
    last_name = models.CharField(max_length=50, verbose_name="фамилия")
    '''пол (1 символ)'''
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="пол")
    '''дата рождения в timestamp (задаётся параметромauto_now_add=True)'''
    birth_date = models.DateTimeField(auto_now_add=True, verbose_name="дата рождения")

    # class Meta:
    #     unique_together = ("id", "email", )
    def __str__(self):
        return '\n id = %s,\n first_name = %s,\n last_name = %s,\n email = %s,\n gender = %s,\n birth_date = %s' % \
               (self.id, self.first_name, self.last_name, self.email, self.gender, self.birth_date)

    def func1(self):
        return self.id == 42


class Visit(models.Model):
    from djchoices import DjangoChoices

    class Mark(DjangoChoices):
        from djchoices import ChoiceItem

        one = ChoiceItem(1)
        two = ChoiceItem(2)
        three = ChoiceItem(3)
        four = ChoiceItem(4)
        five = ChoiceItem(5)

    '''id посещения (устанавливается тестирующей системой)'''  # todo 32р беззн число
    id = models.PositiveIntegerField(primary_key=True)
    '''id достопримечательности'''  # todo 32р беззн число
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # todo cascale ли
    '''id путешественника'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''дата посещения в timestamp (задаётся параметромauto_now_add=True)'''
    visited_at = models.DateTimeField(auto_now_add=True)
    '''оценка 1 .. 5'''
    mark = models.PositiveSmallIntegerField(choices=Mark.choices)

    def __str__(self):
        return 'Sigthseen is: %s, located in %s, user is %s, he visited it in %s, mark is %s' % (
            self.id, self.location, self.user, self.visited_at, self.mark)
