# Generated by Django 5.2.1 on 2025-05-28 10:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_teammember_department_alter_teammember_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='experience',
            field=models.PositiveIntegerField(default=1, help_text='Years of experience'),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('tech_stack', models.CharField(help_text='Comma-separated list of technologies used', max_length=255)),
                ('order', models.PositiveIntegerField(default=0)),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='core.teammember')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('level', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('order', models.PositiveIntegerField(default=0)),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='core.teammember')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
