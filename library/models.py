from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify
from django.utils import timezone
to_tz = timezone.get_default_timezone()

#absolute_url
from django.urls import reverse

#paveiksleliams
from .helper import book_cover_upload
from PIL import Image
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your models here.

#books table
class Book(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to=book_cover_upload, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(editable=False)
    writers = models.ManyToManyField('Writer')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', through="BookTags", blank=True)
    added_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        db_table = 'books'
        ordering = ['-added_at']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if not self.cover:
            super(Book, self).save()
        else:
            self.remove_old_image_on_image_update()
            super(Book, self).save(*args, **kwargs)
            image = Image.open(self.cover)
            (width, height) = image.size
            size = ( 331, 460)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.cover.path)

        print(self.writers.all())
        book = Book.objects.get(id=self.id)
        print("dabar: " + str(book.writers.all()))

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        if self.cover:
            self.cover.delete()

        return super(Book, self).delete(*args, **kwargs)

    def remove_old_image_on_image_update(self):
        #patikrinsim ar update ar insert
        try:
            book = Book.objects.get(id=self.id)
        except Book.DoesNotExist:
            #tokio nera, vadinasi bando insertinti
            return
        if book.cover and self.cover and book.cover != self.cover:
            book.cover.delete()

    def get_absolute_url(self):
        return reverse('library:book_details', args=[str(self.slug)])

    def __str__(self):
        return self.title + ' by ' + str(self.writers.all().first())

    #kiek isviso tagu pridejimu turi knyga, del analitikos
    def get_added_tags_count(self):
        count = 0
        booktags = self.booktags_set.all()
        for booktag in booktags:
            count += booktag.users.all().count()

        return count

    #jeigu nera foto, kad nieko negrazinto
    @property
    def cover_url(self):
        if self.cover and hasattr(self.cover, 'url'):
            return self.cover.url
        else:
            url = static('img/no_cover.jpg')
            return url

#writers table
class Writer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(editable=False)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'writers'
        unique_together = ('name', 'last_name')

    def __str__(self):
        if self.last_name:
            return self.name + ' ' + self.last_name
        else:
            return self.name

    def save(self, *args, **kwargs):
        if self.last_name:
            self.slug = slugify(self.name + ' ' + self.last_name)
        else:
            self.slug = slugify(self.name)
        return super(Writer, self).save(*args, **kwargs)

#tags table
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tags'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

#additional fields for tags on book
class BookTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)

    class Meta:
        db_table = 'booktags'
        unique_together = ('book', 'tag')


#categories table
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)

    class Meta:
        db_table = 'categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

#orders table
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)  #auto_now_add=True
    books = models.ManyToManyField(Book, blank=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.user.username + ' ' + str(self.created_at.astimezone(to_tz))
