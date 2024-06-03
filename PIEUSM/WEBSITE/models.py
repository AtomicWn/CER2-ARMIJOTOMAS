from django.db import models
from django.conf import settings

# Create your models here.

tipo_temas = [
   ("Tema 1" , "Tema 1"),
   ("Tema 2" , "Tema 2"),
   ("Tema 3" , "Tema 3"),
   ("Tema 4" , "Tema 4"),
]

class Propuesta(models.Model):
    nombre = models.CharField(max_length=50)
    estudiante = models.CharField(max_length=50)
    tema = models.CharField(max_length=20, choices=settings.TIPO_TEMAS)
    profesor = models.CharField(max_length=50)
    
    
    def __str__(self) -> str:
        return self.nombre
    