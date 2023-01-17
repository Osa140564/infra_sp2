from datetime import datetime

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from django.db import models
from django.contrib.auth.models import AbstractUser

CURRENT_YEAR = datetime.now().year


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'админ')
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        null=False,
        unique=True
    )
    email = models.EmailField(
        verbose_name='почта пользователя',
        max_length=150,
        null=False,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(max_length=200, blank=True)
    first_name = models.TextField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Строка идентификатор жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Строка идентификатор категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для Произведений."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    year = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Произведение должно быть в н.э."),
            MaxValueValidator(
                CURRENT_YEAR,
                message="Нельзя создать произедение из будущего"
            )
        ]
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']


class GenreTitle(models.Model):
    """Модель для связи ManyToMany, между
    Titles и Genre, она создаст промежуточную таблицу."""
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title} {self.genre}'
