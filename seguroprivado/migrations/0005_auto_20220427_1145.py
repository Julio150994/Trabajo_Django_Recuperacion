# Generated by Django 3.1.2 on 2022-04-27 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seguroprivado', '0004_auto_20220422_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compramedicamento',
            options={'verbose_name': 'compramedicamento', 'verbose_name_plural': 'compramedicamentos'},
        ),
        migrations.AlterModelOptions(
            name='medicamento',
            options={'ordering': ['-id'], 'verbose_name': 'medicamento', 'verbose_name_plural': 'medicamentos'},
        ),
        migrations.AlterModelOptions(
            name='medico',
            options={'ordering': ['-id'], 'verbose_name': 'medico', 'verbose_name_plural': 'medicos'},
        ),
    ]