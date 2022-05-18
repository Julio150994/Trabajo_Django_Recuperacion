# Generated by Django 3.1.2 on 2022-05-18 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguroprivado', '0011_auto_20220518_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='nombre',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='receta',
            field=models.CharField(choices=[('s', 'Con receta'), ('n', 'Venta libre')], default='s', max_length=1, verbose_name='Receta'),
        ),
    ]
