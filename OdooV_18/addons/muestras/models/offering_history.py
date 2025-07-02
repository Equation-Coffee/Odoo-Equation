from odoo import api, fields, models, _

class ResPartnerOfferingHistory(models.Model):
    _name='muestras.offering_history'
    _description='Historico de envios de Ofertable por cliente'

    
    lines = fields.One2many(string="Offering Lines",
        comodel_name='muestras.offering_history_line',
        inverse_name='offering_id',
        copy=True,
        auto_join=True
        )
    partner=fields.Many2one('res.partner',string="Customer")
    date=fields.Date(string="Date")
    expiration_date=fields.Date(string="Expiration Date")
    offering_seq=fields.Char(string="Offering Code")
    salesperson_header=fields.Many2one(comodel_name="res.users",string="Main Salesperson")
    salesperson=fields.Many2one(string="Salesperson ",comodel_name="res.users")
    pdf_file = fields.Binary(string='PDF')
    pdf_filename = fields.Char(string="PDF Name")
    trm=fields.Float(string="USD/COP Exchange Rate")
    price_c = fields.Float(string="Coffee C Price")



