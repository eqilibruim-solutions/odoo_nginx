# -*- coding: utf-8 -*-
# from odoo import http


# class StockMod(http.Controller):
#     @http.route('/stock_mod/stock_mod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_mod/stock_mod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_mod.listing', {
#             'root': '/stock_mod/stock_mod',
#             'objects': http.request.env['stock_mod.stock_mod'].search([]),
#         })

#     @http.route('/stock_mod/stock_mod/objects/<model("stock_mod.stock_mod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_mod.object', {
#             'object': obj
#         })
