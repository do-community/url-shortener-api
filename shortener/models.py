from django.db import models
import random
import string


def prefix_generator(size=8):
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for i in range(size)
    )


class URLRedirect(models.Model):
    short_link = models.CharField(max_length=32, default=prefix_generator, unique=True)
    url = models.URLField(max_length=1024)
    visit_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "URL Redirect"
        verbose_name_plural = "URL Redirects"

    def __str__(self):
        return self.short_link
