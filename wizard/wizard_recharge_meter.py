import logging

from odoo.addons.niot_meter.models.meter import Meter, RECHARGE_API
from odoo import fields, models

_logger = logging.getLogger(__name__)


class WizardCancelFees(models.TransientModel):
    _name = "wizard.recharge.meter"
    _description = "Wizard for recharging the meter"

    amount = fields.Float(required=True, default=0.0)
    imei = fields.Char()
    address = fields.Char()

    def action_recharge_meter(self):
        amount = self.amount * 10

        payload = {
            "address": self.address,
            "imei": self.imei,
            "amount": amount
        }
        Meter.call_endpoint(RECHARGE_API, payload)
