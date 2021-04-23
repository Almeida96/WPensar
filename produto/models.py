from django.db import models

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.nome}'
