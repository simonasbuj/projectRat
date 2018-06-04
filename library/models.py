from django.db import models

#paveiksleliams
from .helper import book_cover_upload
from PIL import Image

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to=book_cover_upload, null=True, blank=True)

    class Meta:
        db_table = 'books'

    def save(self):
        if not self.cover:
            super(Book, self).save()
            return

        self.remove_old_image_on_image_update()

        super(Book, self).save()
        image = Image.open(self.cover)
        (width, height) = image.size
        size = ( 331, 460)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.cover.path)
    
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
