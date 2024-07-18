from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    post_title = models.CharField(max_length = 250)
    post_content = models.TextField()
    published_date = models.DateField(auto_now_add= True)
    
    def __str__(self):
        return self.post_title
    
class Comment(models.Model):
    author_name = models.CharField(max_length = 250)
    comment_content = models.TextField(max_length = 500)
    comment_date = models.DateField(auto_now_add= True)
    post_id = models.ForeignKey(Post, on_delete= models.CASCADE)

    def __str__(self):
        return self.author_name + ' - ' + str(self.post_id)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensure one like per user per post

    def __str__(self):
        return f'{self.user.username} liked {self.post.id}'