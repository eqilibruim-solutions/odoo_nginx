# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class stock_mod(models.Model):
#     _name = 'stock_mod.stock_mod'
#     _description = 'stock_mod.stock_mod'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api

class HelpDeskInherit(models.Model):
    _inherit = "portal"
 
    city = fields.Char(string='Ciudad cliente', related='partner_id.city', store=True)
    street = fields.Char(string='Direccion cliente', related='partner_id.street', store=True)
