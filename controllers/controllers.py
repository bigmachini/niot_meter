# -*- coding: utf-8 -*-
# from odoo import http


# class PowerMeter(http.Controller):
#     @http.route('/power_meter/power_meter', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/power_meter/power_meter/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('power_meter.listing', {
#             'root': '/power_meter/power_meter',
#             'objects': http.request.env['power_meter.power_meter'].search([]),
#         })

#     @http.route('/power_meter/power_meter/objects/<model("power_meter.power_meter"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('power_meter.object', {
#             'object': obj
#         })
