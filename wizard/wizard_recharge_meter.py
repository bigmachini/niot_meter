import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class WizardCancelFees(models.TransientModel):
    _name = "wizard.recharge.meter"
    _description = "Wizard for recharging the meter"

    amount = fields.Float(required=True, default=0.0)

    def action_recharge_meter(self):
        pass
