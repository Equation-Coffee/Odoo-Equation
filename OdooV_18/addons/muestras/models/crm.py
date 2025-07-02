
from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sample_order_id = fields.Many2one(
        'muestras.order', 
        string='Solicitud de Muestra',
        help='La solicitud de muestra asociada a este lead.'
    )

