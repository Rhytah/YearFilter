from django.db import models

class PageYear(models.Model):
    """
    Model for storing page ID and year data.
    """
    page_id = models.PositiveIntegerField(primary_key=True)
    year = models.SmallIntegerField()

    class Meta:
        db_table = 'page_years'
        verbose_name = 'Page Year'
        verbose_name_plural = 'Page Years'
        indexes = [
            models.Index(fields=['year']),
        ]

    def __str__(self):
        return f"Page {self.page_id} - Year {self.year}"