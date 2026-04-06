from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postmodel',
            options={'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AddField(
            model_name='postmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='postmodel',
            name='is_pinned',
            field=models.BooleanField(default=False, verbose_name='Закреплён'),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
