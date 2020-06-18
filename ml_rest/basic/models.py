from django.db import models

class Entry(models.Model):
    STATUS_PENDING = "pending"
    STATUS_EXERCUTED = "executed"
    STATUS_SET = (
            (STATUS_PENDING, "実行待ち"),
            (STATUS_EXERCUTED, "実行完了"),
    )

    code_id = models.IntegerField()
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_SET, default=STATUS_PENDING, max_length=8)
