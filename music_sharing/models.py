from django.db import models


class AudioFile(models.Model):
    file = models.FileField()
    content_type = models.CharField(null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        self.content_type = self.file.file.content_type
        super().save(*args, **kwargs)
