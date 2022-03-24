# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPickinInherit(models.Model):
    _inherit = "stock.picking"

    city = fields.Char(string='Ciudad', related='partner_id.city', store=False, copy=True, check_company=True)
    street2 = fields.Char(string='Direccion', related='partner_id.street2', store=False, copy=False)
    