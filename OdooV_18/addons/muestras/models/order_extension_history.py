from odoo import api, fields, models, _

class OrderExtension(models.Model):
    _name='muestras.order_extension'
    _description='Historic Extension of the Order Due Date'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    
    order_id = fields.Many2one('muestras.order',string="Order")
    previous_deadline = fields.Date(string="Previous Deadline")
    new_deadline = fields.Date(string="New Deadline")
    date_difference = fields.Integer(string="Days Difference")
    order_extension_reason = fields.Many2one('muestras.extension_reason',string='Extension Reason')
    notes = fields.Text(string='Notes')
    user_id = fields.Many2one('res.users',string='Requested by')




