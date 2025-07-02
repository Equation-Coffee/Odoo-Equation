from odoo import models, fields, api
import csv
import os
import logging
from odoo.exceptions import ValidationError

# Configuración del loggerdd
_logger = logging.getLogger(__name__)

class Parametros(models.Model):
    _name = "muestras.parametros"
    _description = "Parámetros de muestras"
    _rec_name="code"
    code = fields.Char(string="Código Producto",compute="_compute_code",store=True)
    project = fields.Char(string="Proyecto", required=True)
    category = fields.Char(string="Categoría", required=True)
    program = fields.Text(string="Programa", required=True)
    percentUSA = fields.Float(string = "Porcentaje USA",default=1.0)
    percentEU = fields.Float(string = "Porcentaje EU")
    percentAsia = fields.Float(string = "Porcentaje Asia")
    



    @api.constrains('percentUSA','percentEU','percentAsia')
    def _cheksum_percent(self):
        for record in self:
                total_sum = record.percentUSA + record.percentEU + record.percentAsia
                if total_sum !=1:
                    raise ValidationError("La suma de los campos debe ser exactamente 1.Actualmente es{:.2f}".format(total_sum))


    @api.depends('project','category','program')
    def _compute_code(self):
        for record in self:
            record.code = str(record.project)+str(record.category)+str(record.program)

    @api.model    
    def parametersLoad(self):
        file_path = '/mnt/extra-addons/muestras/data/parametros.csv'
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('project') and row.get('variety') and row.get('category'):
                        record = self.create({
                            'project': row['project'],
                            'program': row['program'],
                            'category': row['category'],
                        })
                        _logger.info(f"Registro creado :{record.id}")
                    else:
                        _logger.warning(f"Fila incompleta: {row}")
            _logger.info("Datos cargados exitosamente desde inventarioprueba.csv")
        except FileNotFoundError:
            _logger.error(f"No se encontró el archivo: {file_path}")
        except Exception as e:
            _logger.error(f"Error al cargar los datos: {str(e)}")
