
from odoo import models, fields, api


class Tarrif(models.Model):
    _name = 'meter.tariff'
    _description = 'Power Meter Tariff'

    name = fields.Char(required=True)
    amount = fields.Float(required=True)
    active = fields.Boolean(default=True, required=True)
