from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Topic(models.Model):
    name = models.CharField(max_length=200)
    auth_required = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=5)

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return '/{}/ - {}'.format(self.slug, self.name)


class Thread(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    # Is an OP thread if empty
    ancestor_id = models.ForeignKey('self', related_name='posts', null=True, blank=True)
    parent_id = models.ForeignKey('self', related_name='replies', null=True, blank=True)

    author_name = models.CharField(max_length=50, blank=True, null=True)
    author_email = models.EmailField(blank=True, null=True)

    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()

    file = models.FileField(blank=True, null=True)

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '#{} | {}  Created at {}. Ancestor {}. Parent {}.'.format(self.pk, self.subject,
                                                                             self.created_date, self.ancestor_id,
                                                                             self.parent_id)

    @property
    def author(self):
        if self.author_name is None or self.author_name is '':
            return 'Anonymous'
        else:
            return self.author_nam

    @property
    def heading(self):
        if self.subject:
            return self.subject
        else:
            content = self.message.split()
            return ' '.join(content[:5]) + '...'
