# Generated by Django 2.1.4 on 2019-03-18 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20190315_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='comment_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_obj', related_query_name='comment_obj', to='backend.Comment'),
        ),
        migrations.AddField(
            model_name='like',
            name='post_obj',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_obj', related_query_name='post_obj', to='backend.Post'),
        ),
        migrations.AlterField(
            model_name='like',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', related_query_name='owner', to='backend.Author'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('author', 'comment_obj'), ('author', 'post_obj')},
        ),
    ]
