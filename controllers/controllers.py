# -*- coding: utf-8 -*-
from odoo import http

# class Mi(http.Controller):
#     @http.route('/mi/mi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mi/mi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mi.listing', {
#             'root': '/mi/mi',
#             'objects': http.request.env['mi.mi'].search([]),
#         })

#     @http.route('/mi/mi/objects/<model("mi.mi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mi.object', {
#             'object': obj
#         })