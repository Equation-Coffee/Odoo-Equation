from odoo import models, fields, api

class Proyecto(models.Model):
    _name="muestras.project"
    _description="Prpyectos"
    name=fields.Char(string="Proyect Name")
        