from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Post(models.Model):
    titles = models.CharField(max_length=100)
    contents = models.TextField()
    image_urls = models.ImageField(null=True, upload_to="posts/images")
    created_at = models.DateTimeField(auto_now_add=True)
    slug  = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.ManyToManyField(User, related_name='views', blank=True)




    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titles)
        super().save(*args, **kwargs)

    @property
    def formatted_image_urls(self):
        url = self.image_urls if self.image_urls.__str__().startswith(('http://', 'https://')) else self.image_urls.url
        return url    


    def total_likes(self):
        return self.likes.count()
    
    def total_views(self):
        return self.views.count()

    def __str__(self):
        return self.titles
    

class AboutUs(models.Model):
    content = models.TextField()    


class PostComments(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    name =    models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"comment by {self.name} on {self.post.titles}"