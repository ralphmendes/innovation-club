from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField()
    category = models.CharField(max_length=120)
    image = models.ImageField(upload_to='posts',blank=True,null=True)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"pk": self.pk})
    
    def total_upvotes(self):
        return self.votes.filter(vote=1).count()

    def total_downvotes(self):
        return self.votes.filter(vote=-1).count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username
    
class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    vote = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])  # Change from TextField to IntegerField
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.author.username, self.get_vote_display())
    
    

    
