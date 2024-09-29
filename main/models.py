from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ArtWork(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    image = models.ImageField(upload_to='artworks/')  # Убедитесь, что указываете upload_to
    title = models.CharField(max_length=25)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):  # Исправлено на Comment
    artwork = models.ForeignKey(ArtWork, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()  # Добавлено поле для текста комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Автоматическое заполнение даты создания
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.artwork}"

