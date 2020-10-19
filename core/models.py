from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from dirtepol import settings

ASSET_CHOICES = (
    ('AST', 'Bien'),
    ('AUX', 'Bien auxiliar'),
    ('OTH', 'Sobrantes'),
)

PROPERTY_STATE_CHOICES = (
    ('A', 'Alquilado'),
    ('P', 'Propio'),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Actualizado en')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nombre')
    email = models.EmailField(blank=False, unique=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Asset(BaseModel):
    asset_type = models.CharField(max_length=3, choices=ASSET_CHOICES, default='AST')
    pat_code = models.CharField(max_length=255, null=True, verbose_name='Cód patrimonial')
    internal_code = models.CharField(max_length=255, null=True, verbose_name='Cód. interno')
    name = models.CharField(max_length=255, verbose_name='Descripción')
    brand = models.CharField(max_length=255, verbose_name='Marca')
    model = models.CharField(max_length=255, verbose_name='Modelo')
    color = models.CharField(max_length=255, verbose_name='Color')
    size = models.CharField(max_length=255, verbose_name='Dimensiones')
    conservation = models.CharField(max_length=255, verbose_name='Estado de conservación')
    observation = models.TextField(verbose_name='Observaciones')
    is_auxiliary = models.BooleanField(default=False, verbose_name='¿Es un bien auxiliar?')

    class Meta:
        verbose_name = 'Bien'
        verbose_name_plural = 'Bienes'

    def __str__(self):
        return self.name


class RealState(BaseModel):
    dependency = models.CharField(max_length=255, null=True, verbose_name='Dependencia')
    address = models.CharField(max_length=255, null=True, verbose_name='Domicilio')
    urb = models.CharField(max_length=255, null=True, verbose_name='Urbanización')
    district = models.CharField(max_length=255, null=True, verbose_name='Distrito/Provincia')
    department = models.CharField(max_length=255, null=True, verbose_name='Departamento')
    has_registry_info = models.BooleanField(default=True,
                                            verbose_name='Cuenta con saneamiento físico legal (información registral)')
    procedure_date = models.DateField(default=timezone.now, verbose_name='Fecha de inicio del trámite')
    registry_area = models.CharField(max_length=255, null=True,
                                     verbose_name='Area encargada del saneamiento físico legal')
    property_state = models.CharField(max_length=2, choices=PROPERTY_STATE_CHOICES, default='P')
    rent_amount = models.DecimalField(default=0.00, max_digits=14, decimal_places=2,
                                      verbose_name='Monto de alquiler mensual')
    maintenance_amount = models.DecimalField(default=0.00, max_digits=14, decimal_places=2,
                                             verbose_name='Monto de mantenimeinto mensual')
    construction_date = models.DateField(default=timezone.now, verbose_name='Año de construcción del inmueble')
    persons = models.PositiveIntegerField(default=0, verbose_name='Nñumero de personas que laboran')
    area = models.DecimalField(default=0.00, max_digits=14, decimal_places=2, verbose_name='Área total del terreno')
    built_area = models.DecimalField(default=0.00, max_digits=14, decimal_places=2,
                                     verbose_name='Área total construida')
    is_planned_use = models.BooleanField(default=True,
                                         verbose_name='Local planificado para ser usado como (Vivienda, almacen Base operativa, Oficina Administrativa, Taller, etc')
    is_corrected_use = models.BooleanField(default=True, verbose_name='El local se usa para lo que fue construido')
    has_civil_defense = models.BooleanField(default=True, verbose_name='Cuenta con Inspeccion de Defensa Civil')
    last_civil_defense_inspection = models.DateField(default=timezone.now,
                                                     verbose_name='Ultima fecha de Inspeccion de Defensa Civil')

    class Meta:
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'

    def __str__(self):
        return f"{self.dependency} - {self.address}"


class Vehicle(BaseModel):
    pat_code = models.CharField(max_length=255, null=True, verbose_name='Cód patrimonial')
    internal_code = models.CharField(max_length=255, null=True, verbose_name='Cód. interno')
    internal_plate = models.CharField(max_length=255, verbose_name='Placa interna')
    rod_plate = models.CharField(max_length=255, verbose_name='Placa de rodaje')
    type = models.CharField(max_length=255, verbose_name='Tipo')
    brand = models.CharField(max_length=255, verbose_name='Marca')
    model = models.CharField(max_length=255, verbose_name='Modelo')
    year = models.CharField(max_length=255, verbose_name='Año')
    fuel = models.CharField(max_length=255, verbose_name='Combustible')
    chassis = models.CharField(max_length=255, verbose_name='Chasis')
    motor_number = models.CharField(max_length=255, verbose_name='Núm. de motor')
    cylinders = models.PositiveSmallIntegerField(default=1, verbose_name='Núm. de cilindros')
    conservation = models.CharField(max_length=255, verbose_name='Estado de conservación')
    soat = models.BooleanField(default=False, verbose_name='¿Tiene SOAT?')
    car_insurance = models.BooleanField(default=False, verbose_name='¿Tiene seguro?')
    is_active = models.BooleanField(default=False, verbose_name='¿Está operativo?')
    observation = models.TextField(verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.brand} {self.model} {self.rod_plate}"
