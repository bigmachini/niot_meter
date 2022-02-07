import logging

from odoo.addons.niot_meter.models.meter import Meter, RECHARGE_API
from odoo import fields, models

_logger = logging.getLogger(__name__)


class WizardCancelFees(models.TransientModel):
    _name = "wizard.recharge.meter"
    _description = "Wizard for recharging the meter"

    amount = fields.Float(required=True, default=0.0)
    meter_id = fields.Many2one('power.meter')

    def action_recharge_meter(self):
        payload = {
            "address": self.meter_id.get_formatted_address(),
            "imei": self.meter_id.imei,
            "amount": self.amount
        }
        Meter.call_endpoint(RECHARGE_API, payload)
