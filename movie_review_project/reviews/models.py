from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='rating_valid_range')
        ]
    
    def __str__(self):
        return f'{self.movie_title} - {self.rating}/5'
