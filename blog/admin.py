from django.contrib import admin
from .models import Post, Topic, SubTopic, Thread

admin.site.register(Post)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Thread)