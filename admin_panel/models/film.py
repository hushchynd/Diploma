from django.core import validators
from django.db import models
import django.forms as forms


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "countries"

    def __str__(self):
        return self.name


class Operator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "operators"


class Editor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "editors"


class Producer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "producers"


class ScriptWriter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "scriptwriters"


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "genres"


class Film(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Название", validators=[
        validators.MaxLengthValidator(20),
        validators.RegexValidator('^[A-ZА-Я]{1}.*', message='Название должно начинаться с заглавной буквы'),
        validators.ProhibitNullCharactersValidator(),
    ])
    description = models.TextField(verbose_name="Описание",
                                   validators=[
                                       validators.MaxLengthValidator(500),
                                       validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                 message='Описание должно начинаться с заглавной буквы.'),
                                       validators.ProhibitNullCharactersValidator(),

                                   ])
    card_img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                                 verbose_name="Картинка карточки",
                                 validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    released = models.DateField(verbose_name="Дата выхода")
    trailer_link = models.URLField(max_length=100, verbose_name="Ссылка на трейлер",
                                   validators=[validators.URLValidator(),
                                               validators.RegexValidator(
                                                   '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)',
                                                   message='Неверный url адресс')
                                               ],
                                   )
    banner = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True,
                               verbose_name="Баннер",
                               validators=[validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])])
    year = models.PositiveSmallIntegerField(verbose_name="Год",
                                            validators=[
                                                validators.MaxValueValidator(2100),
                                                validators.MinValueValidator(1900),
                                            ])
    countries = models.ManyToManyField(Country, verbose_name="Страны")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    producers = models.ManyToManyField(Producer, verbose_name="Продюсеры")
    editors = models.ManyToManyField(Editor, verbose_name="Режисёры")
    scriptwriters = models.ManyToManyField(ScriptWriter, verbose_name="Сценаристы")
    operators = models.ManyToManyField(Operator, verbose_name="Операторы")
    budget = models.PositiveIntegerField(verbose_name="Бюджет")
    legal_age = models.PositiveSmallIntegerField(verbose_name="Мин Возраст",
                                                 validators=[
                                                     validators.MaxValueValidator(18),
                                                     validators.MinValueValidator(8),
                                                 ])
    duration = models.PositiveSmallIntegerField(verbose_name="Длительность",
                                                validators=[
                                                    validators.MinValueValidator(10),
                                                ])
    technology_types = models.ManyToManyField('TechnologyType', verbose_name="Форматы")
    seo_block = models.OneToOneField('SeoBlock', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = "films"


class TechnologyType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'technology_type'

    def __str__(self):
        return self.name


class FilmImg(models.Model):
    img = models.ImageField(upload_to="photos/%Y/%m/%d/", max_length=100, unique=True, null=True, verbose_name='',
                            validators=[
                                validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])
                            ]
                            )
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    class Meta:
        db_table = 'film_imgs'


class SeoBlock(models.Model):
    url = models.URLField(verbose_name='Ссылка',
                          validators=[
                              validators.URLValidator(),
                              validators.RegexValidator(
                                  '\w*:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&\/=]*)',
                                  message='Неверный url')
                          ],
                          )
    title = models.CharField(max_length=50, verbose_name='Название',
                             validators=[
                                 validators.MaxLengthValidator(50, 'Название не более 20ти символов.'),
                                 validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                           'Название должно начинаться с заглавной буквы'),
                                 validators.ProhibitNullCharactersValidator(),
                             ]
                             )
    seo_description = models.TextField(verbose_name='Описание', null=True,
                                       validators=[
                                           validators.RegexValidator('^[A-ZА-Я]{1}.*',
                                                                     message='Описание должно начинаться с заглавной буквы'),
                                           validators.ProhibitNullCharactersValidator(),
                                       ]
                                       )
    keywords = models.CharField(verbose_name='Ключевые слова', max_length=255,
                                validators=[
                                    validators.MaxLengthValidator(255),
                                    validators.ProhibitNullCharactersValidator(),
                                ]
                                )

    class Meta:
        db_table = 'seo_block'
