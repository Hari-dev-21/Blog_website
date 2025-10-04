
from blog.models import Post, Category
from typing import Any
import random

from django.core.management.base import BaseCommand




class Command(BaseCommand):
    help = "this command inserts post data"
    def handle(self, *args: Any, **options: Any):


      #delete existing data
      # 
      Post.objects.all().delete() 

      titles = [
"The Future of AI",
"Climate Change Solutions",
"Remote Work Trends",
"Quantum Computing Explained",
"Renewable Energy Innovations",
"Deep Learning Demystified",
"Post-Pandemic Economic Outlook",
"Blockchain in Finance",
"Storytelling in Marketing",
"Medical Technology Advances",
"Space Exploration Challenges",
"Psychology of Decision Making",
"Evolution of Social Media",
"The Art of Cooking",
"Cultural Diversity in Society",
# "Sustainable Development Investments",
# "Globalization Impact",

]

      contents =[
    "Exploring the future of artificial intelligence and its impact on society.",
"Discovering solutions to combat climate change and protect the environment.",
"Analyzing trends and challenges in remote work environments.",
"An introduction to the principles and applications of quantum computing.",
"Investigating the latest innovations in renewable energy sources.",
"Understanding the fundamentals of deep learning and neural networks.",
"Examining the economic landscape in the aftermath of the COVID-19 pandemic.",
"[xploring the potential of blockchain technology in the financial sector.",
"Harnessing the power of storytelling to create compelling marketing campaigns.",
"Highlighting breakthroughs and advancements in medical technology.",
"Addressing the obstacles and opportunities in space exploration.",
"Exploring the psychological factors influencing decision-making processes.",
"Tracing the evolution of social media platforms and their impact on society.",
"Celebrating the art of cooking and culinary creativity.",
"Promoting inclusivity and embracing diversity in modern communities.",
# "Examining the effects of globalization on local and global economies.",
]

      image_urls = [

# "https://picsum. photos/id/4/800/400"
"https://picsum.photos/id/1/800/400",
"https://picsum.photos/id/2/800/400",   
"https://picsum.photos/id/3/800/400",
"https://picsum.photos/id/4/800/400",
"https://picsum.photos/id/5/800/400",
"https://picsum.photos/id/6/800/400",
"https://picsum.photos/id/7/800/400",
"https://picsum.photos/id/8/800/400",
"https://picsum.photos/id/9/800/400",
"https://picsum.photos/id/10/800/400",
"https://picsum.photos/id/11/800/400",
"https://picsum.photos/id/12/800/400",
"https://picsum.photos/id/13/800/400",
"https://picsum.photos/id/14/800/400",
"https://picsum.photos/id/15/800/400",
]
      categories = Category.objects.all()

      for title, content, img_url in zip(titles, contents, image_urls):
        category = random.choice(categories)
        post = Post(titles=title, contents=content, image_urls=img_url, category=category)
        post.save()  

      self.stdout.write(self.style.SUCCESS("completed inserting Data"))    
