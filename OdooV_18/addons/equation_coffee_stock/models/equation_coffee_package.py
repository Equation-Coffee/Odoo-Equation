# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

## NO ESTA INCLUIDO EN EL INIT 
_logger = logging.getLogger(__name__)


class EquationCoffeeLotPackage(models.Model):

    _name = 'equation.coffee_lot_package'
    _description = 'Lot Package'
    _rec_name = 'package'



    package=fields.Char(string='Empaquetado')
