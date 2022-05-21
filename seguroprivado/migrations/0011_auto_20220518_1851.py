# Generated by Django 3.1.2 on 2022-05-18 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguroprivado', '0010_auto_20220518_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='receta',
            field=models.CharField(choices=[('Con receta', 's'), ('Venta libre', 'n')], default='s', max_length=11, verbose_name='Receta'),
        ),
    ]