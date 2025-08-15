from odoo import api, fields, models

class ParentKanban(models.Model):
    _name='crm.parent_kanban'
    _inherit='crm.lead'
    _description = 'Kanban Externo'

    name = fields.Char(required=True)
    etapa_id = fields.Many2one("crm.stage",required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    tag_ids = fields.Many2many(
        'crm.tag', 'crm_parent_kanban_tag_rel', 'parent_kanban_id', 'tag_id', string="Tags")





class ParentStage(models.Model):
    _name='crm.parent_stage'
    _order = 'sequence,id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string="Folded in Kanban")
