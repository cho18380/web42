from django.contrib.auth.models import User
from django.db import models



board_choices = (
        ('daretalk', 'Dare Talk'),
        ('labnewsroom', '연구소 뉴스룸'),
        ('projectex', '프로젝트 사례 공유'),
        ('announce', '공지사항'),
        ('info', '생활정보'),
        ('ref', '자료실'),
        ('weeklynews', 'Weekly News'),
        ('ceotalk', 'CEO TALK'),
        ('client', '고객사 동향'),
        ('forum', '토론방'),
    )


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    board_name = models.CharField(max_length=30, choices= board_choices, default='announce')
    imgfile = models.ImageField(null=True, upload_to="media/", blank=True) # 이미지 컬럼 추가
    
    def __str__(self):
        return self.subject


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    
