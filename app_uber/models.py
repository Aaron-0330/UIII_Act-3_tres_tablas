# app_uber/models.py

from django.db import models

# ==========================================
# MODELO: Chofer
# ==========================================
class Chofer(models.Model):
    id_chofer = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    edad = models.IntegerField()
    fecha_ingreso = models.DateField()

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO: Usuario_pasajero
# ==========================================
class UsuarioPasajero(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=150)
    fecha_registro = models.DateField()
    genero = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# ==========================================
# MODELO: Viaje
# ==========================================
class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    hora_salida = models.TimeField()
    duracion = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=8, decimal_places=2)
    estatus = models.CharField(max_length=20)

    # 🔹 Relación 1:N con Chofer
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, related_name='viajes')

    # 🔹 Relación N:M con UsuarioPasajero
    pasajeros = models.ManyToManyField(UsuarioPasajero, related_name='viajes')

    def __str__(self):
        return f"Viaje a {self.destino} con {self.chofer.nombre}"