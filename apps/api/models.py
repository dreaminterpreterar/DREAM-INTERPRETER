from django.db import models

class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='nombre', unique=True)
    description = models.CharField(max_length=100, verbose_name='descripcion')
    value = models.TextField(verbose_name='valor')

    class Meta:
        verbose_name_plural = 'parametros'
        verbose_name = 'parametro'

    def __str__(self):
        return f"PARAMETRO: {self.name.upper()}."


class Interpretation(models.Model):
    user = models.CharField(max_length=10, verbose_name='usuario')
    dream = models.TextField(verbose_name='sueño')
    interpretation = models.TextField(verbose_name='interpretacion')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creacion')

    class Meta:
        verbose_name_plural = 'interpretaciones'
        verbose_name = 'interpretacion'
        ordering = ['-created_at']

    def __str__(self):
        created_at_str = self.created_at.strftime('%d/%m/%Y %H:%M')
        return f"INTERPRETACION DEL USUARIO CON ID: {self.user.upper()} CREADA EL: {created_at_str}."