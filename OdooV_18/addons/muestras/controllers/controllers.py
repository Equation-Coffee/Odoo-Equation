# -*- coding: utf-8 -*-
# from odoo import http


# class Muestras(http.Controller):
#     @http.route('/muestras/muestras', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/muestras/muestras/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('muestras.listing', {
#             'root': '/muestras/muestras',
#             'objects': http.request.env['muestras.muestras'].search([]),
#         })

#     @http.route('/muestras/muestras/objects/<model("muestras.muestras"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('muestras.object', {
#             'object': obj
#         })
