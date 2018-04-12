from django.db import models
from django.utils import timezone
from django.urls import reverse, reverse_lazy

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete ='CASCADE',) #Since this is not a multiuser blog (superusers only can be authors)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    create_date = models.DateTimeField(default = timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment = True)

    def get_absolute_url(self): #must be named this
        return reverse("post_detail", kwargs= {'pk': self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name = 'comment',on_delete ='CASCADE',) # each comment aligns with a given Post
    author = models.CharField(max_length=200) #author of the comment is not the same as author of the Post
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default = False) #make sure this matches your approved_comment variable in the Post class

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return('post_list')

    def __str__(self):
        return self.text
