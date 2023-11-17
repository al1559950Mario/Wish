from django.test import TestCase
from .models import MiModelo

class MiModeloTestCase(TestCase):
    def test_creacion_de_modelo(self):
        # Crea una instancia del modelo con datos en formato JSON
        datos = {'clave1': 'valor1', 'clave2': 'valor2'}
        modelo = MiModelo(data=datos)
        modelo.save()

        # Recupera el modelo de la base de datos
        modelo_recuperado = MiModelo.objects.get(pk=modelo.pk)

        # Verifica que los datos en formato JSON sean los mismos
        self.assertEqual(modelo_recuperado.data, datos)
