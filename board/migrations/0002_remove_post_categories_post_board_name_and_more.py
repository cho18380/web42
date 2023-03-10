# Generated by Django 4.1.6 on 2023-02-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AddField(
            model_name='post',
            name='board_name',
            field=models.CharField(choices=[('daretalk', 'Dare Talk'), ('labnewsroom', '연구소 뉴스룸'), ('projectex', '프로젝트 사례 공유'), ('announce', '공지사항'), ('info', '생활정보'), ('ref', '자료실'), ('weeklynews', 'Weekly News'), ('ceotalk', 'CEO TALK'), ('client', '고객사 동향'), ('forum', '토론방')], default='announce', max_length=30),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
