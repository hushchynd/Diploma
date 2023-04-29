import os

from django.core import validators
from django.db import models


class TemplateHtml(models.Model):
    template_html = models.FileField(verbose_name="Html шаблон",upload_to='templates_html',)
    date_uploaded = models.DateTimeField(verbose_name="Дата создания",auto_now_add=True,)

    def filename(self):
        return os.path.basename(self.template_html.name)
    class Meta:
        db_table = 'template_html'
        ordering = ["-date_uploaded"]
