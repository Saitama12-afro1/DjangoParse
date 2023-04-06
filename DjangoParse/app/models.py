from django.db import models

class Purchase(models.Model):

    purchase_number = models.CharField(primary_key = True, max_length=100)
    start_price = models.DecimalField(max_digits=30, decimal_places=2)
    
    class Meta:
        verbose_name = "purchase"
        verbose_name_plural = "purchases"
        default_related_name = "purchases"
        db_table = "purchases"

    def __str__(self):
        return  f" {self.purchase_number} {self.start_price}"


class Detail(models.Model):
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    calculation = models.DecimalField(max_digits=31, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.calculation = self.purchase.start_price * 10
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "detail"
        verbose_name_plural = "details"
        default_related_name = "details"
        db_table = "details"

    def __str__(self):
        return self.name

    
        
