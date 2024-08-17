# Generated by Django 5.0.2 on 2024-08-17 21:50

import core.validators
import django.utils.timezone
import users.manager
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=150,
                        unique=True,
                        validators=[core.validators.username_validator],
                        verbose_name="Логин пользователя",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        max_length=150,
                        validators=[core.validators.name_validator],
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        validators=[core.validators.name_validator],
                        verbose_name="Отчество",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=150,
                        validators=[core.validators.name_validator],
                        verbose_name="Фамилия пользователя",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        unique=True,
                        validators=[core.validators.validate_mobile],
                        verbose_name="Телефон",
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="День Рождения пользователя"
                    ),
                ),
                (
                    "role",
                    models.TextField(
                        choices=[("user", "User"), ("admin", "Admin")],
                        default="user",
                        max_length=20,
                        verbose_name="Пользовательская роль юзера",
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        blank=True,
                        choices=[("М", "Male"), ("Ж", "Female")],
                        max_length=6,
                        null=True,
                        verbose_name="Пол",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ("-id",),
            },
            managers=[
                ("objects", users.manager.UserManager()),
            ],
        ),
    ]
