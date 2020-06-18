from django.db import models

class CodeElement(models.Model):
    title = models.CharField("title", max_length=255)
    code = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CodeMeta(models.Model):
    meta = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    code = models.ForeignKey(CodeElement, on_delete=models.CASCADE)
