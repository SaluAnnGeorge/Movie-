from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/')  

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_name

    
 
class Feedback1(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s feedback on {self.movie.title}"