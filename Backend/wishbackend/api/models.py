from django.db import models
import subprocess
import json
import os
import sys
import threading

class Categories(models.Model):
    product_description = models.CharField(max_length=255)
    excludes = models.JSONField(null=True, blank=True)
    weighting_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = "Categories"

    #Ejecutar un script de python despues de crear una categoria, el script se llama Recommender_system.py, se encuentra una carpeta arriba de la carpeta del proyecto
    def save(self, *args, **kwargs):
        super(Categories, self).save(*args, **kwargs)
        script_path = "../Recommender_system.py"
        product_description = self.product_description
        excludes = json.dumps(self.excludes)  # Convierte la lista a una cadena en formato JSON
        weighting_type = self.weighting_type
        recommendations = [] 
        command = [sys.executable, script_path, product_description, excludes, weighting_type]
        # Define una función para leer y mostrar la salida
        def reader(pipe, container, func):
            for line in iter(pipe.readline, ''):
                container.append(line)
                func(line)
            pipe.close()

        # Ejecuta el comando
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Crea y comienza los hilos para leer la salida
        output = []
        errors = []
        thread_out = threading.Thread(target=reader, args=[process.stdout, output, sys.stdout.write])
        thread_err = threading.Thread(target=reader, args=[process.stderr, errors, sys.stderr.write])
        thread_out.start()
        thread_err.start()

        # Espera a que el proceso termine
        process.wait()

        # Espera a que los hilos terminen
        thread_out.join()
        thread_err.join()

        # Comprueba si el comando se ejecutó con éxito
        if process.returncode != 0:
            print("Error al ejecutar el script:", ''.join(errors))
        else:
            recommendations = json.loads(''.join(output))
            print("Recomendaciones:", recommendations)
            rec = Recommendations(data=recommendations)
            rec.save()

class Products(models.Model):
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Products"

class Recommendations(models.Model):
    data = models.JSONField()
    #created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Recommendations"