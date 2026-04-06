from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    posts_postmodel.likes — старая INTEGER колонка (NOT NULL).
    posts_postmodel_likes — M2M таблица уже существует в БД физически.

    Шаг 1: удаляем INTEGER колонку likes из posts_postmodel (реальная операция).
    Шаг 2: регистрируем M2M поле в состоянии Django без создания таблицы
            (таблица posts_postmodel_likes уже есть).
    """

    dependencies = [
        ('posts', '0003_alter_postmodel_options_alter_postmodel_created_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Удаляем старую INTEGER колонку из таблицы
        migrations.RemoveField(
            model_name='postmodel',
            name='likes',
        ),
        # Регистрируем M2M в state Django, но НЕ создаём таблицу физически
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='postmodel',
                    name='likes',
                    field=models.ManyToManyField(
                        blank=True,
                        related_name='liked_posts',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            database_operations=[],  # таблица уже существует — ничего не делаем
        ),
    ]
