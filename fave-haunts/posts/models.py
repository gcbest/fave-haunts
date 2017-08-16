from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=200)
	url = models.TextField()
	topic = models.CharField(max_length=100)
	pub_date = models.DateTimeField()
	# to connect the posts to a specific user
	author = models.ForeignKey(User)
	votes_total = models.IntegerField(default=1)

	def __str__(self):
		return self.title

	def pub_date_pretty(self):
		return self.pub_date.strftime('%b %e %Y')

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.post.title