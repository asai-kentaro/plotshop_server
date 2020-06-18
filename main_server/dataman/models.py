from django.db import models
from codeman.models import CodeElement

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    version = models.CharField(max_length=20, default='v1.0')
    remark = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

class FileCodeLink(models.Model):
    code = models.ForeignKey(CodeElement, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

class DataChank(models.Model):
    name = models.CharField(max_length=256)
    data = models.TextField()
    version = models.CharField(max_length=20, default='1.0')
    timestamp = models.DateTimeField(auto_now_add=True)
