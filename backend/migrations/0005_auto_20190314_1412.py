# Generated by Django 2.1.4 on 2019-03-14 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_post_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_public', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Author')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Source'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comments', to='backend.Post'),
        ),
    ]
