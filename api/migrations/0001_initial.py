# Generated by Django 4.2.11 on 2025-04-10 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PageYear',
            fields=[
                ('page_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('year', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': 'Page Year',
                'verbose_name_plural': 'Page Years',
                'db_table': 'page_years',
                'indexes': [models.Index(fields=['year'], name='page_years_year_696b0e_idx')],
            },
        ),
    ]
