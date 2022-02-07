import json

from odoo import api, models, fields, _

BASE_URL = "http://pl.numeraliot.com:8010/meter"
POWER_API = "/power"
MODE_API = "/mode"
CLEAR_BALANCE_API = "/clear_balance"
BALANCE_API = "/balance"
RECHARGE_API = "/recharge"


class Meter(models.Model):
    _name = 'power.meter'
    _inherit = 'mail.thread'

    _description = 'Model that holds meter details'

    name = fields.Char()
    imei = fields.Char(required=True, tracking=True)
    serial_no = fields.Char(required=True, tracking=True)
    address = fields.Char(required=True, tracking=True)
    power_status = fields.Boolean(required=True, default=False, tracking=True)
    mode = fields.Selection([('prepaid', 'PREPAID'), ('postpaid', 'POSTPAID')], tracking=True,
                            default='prepaid')
    user_id = fields.Many2one('res.partner')
    units = fields.Float(required=True, tracking=True, default=0.0)
    _sql_constraints = [
        ('imei_unique', 'unique (imei)', "IMEI already exists!"),
        ('serial_no_unique', 'unique (serial_no)', "Serial No already exists!"),
        ('address_unique', 'unique (address)', "Address already exists!"),
        ('meter_unique', 'unique (imei,address)', "Meter already exists!"),
    ]

    def get_formatted_address(self):
        address_list = []
        len_address = x = len(self.address)
        for i in range(0, len_address, 2):
            address_list.append(self.address[x - 2: x])
            x -= 2
        return ''.join(address_list)

    @staticmethod
    def call_endpoint(_api, payload):
        import requests
        url = BASE_URL + _api
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200 and response.json()['result']:
            return True
        return False

    def set_power_status(self, status):
        return {
            "address": self.get_formatted_address(),
            "imei": self.imei,
            "status": status
        }

    def set_mode(self, mode):
        return {
            "address": self.get_formatted_address(),
            "imei": self.imei,
            "mode": mode
        }

    def set_balance(self, units=0.00, clear_balance=False):
        if clear_balance:
            return {
                "address": self.get_formatted_address(),
                "imei": self.imei,
            }
        else:
            return {
                "address": self.get_formatted_address(),
                "imei": self.imei,
                "amount": units
            }

    def get_balance(self):
        return {
            "address": self.get_formatted_address(),
            "imei": self.imei,
            "mode": self.mode
        }

    def action_power_on(self):
        payload = self.set_power_status('on')
        if self.call_endpoint(POWER_API, payload):
            self.power_status = True

    def action_power_off(self):
        payload = self.set_power_status('off')
        if self.call_endpoint(POWER_API, payload):
            self.power_status = False

    def action_prepaid(self):
        payload = self.set_mode('prepaid')
        if self.call_endpoint(MODE_API, payload):
            self.mode = 'prepaid'

    def action_post_paid(self):
        payload = self.set_mode('postpaid')
        if self.call_endpoint(MODE_API, payload):
            self.mode = 'postpaid'

    def action_clear_balance(self):
        payload = self.set_balance(clear_balance=True)
        if self.call_endpoint(CLEAR_BALANCE_API, payload):
            self.units = 0.0

    def action_get_balance(self):
        payload = self.get_balance()
        if self.call_endpoint(BALANCE_API, payload):
            self.units = 0.0

    def action_recharge_meter(self):
        view = self.env.ref('niot_meter.wizard_recharge_meter_form')
        # TDE FIXME: a return in a loop, what a good idea. Really.
        return {
            'name': _('Recharge Power Meter'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.recharge.meter',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_imei': self.imei, 'default_address': self.address}
        }


class MeterAssignment(models.Model):
    _name = 'meter.assignment'
    _description = 'Meter assignment history'

    meter_id = fields.Many2one('power.meter')
    user_id = fields.Many2one('res.partner')
    data_assigned = fields.Datetime()
    date_unassigned = fields.Datetime()
    assigned_by = fields.Many2one('res.partner')
    unassigned_by = fields.Many2one('res.partner')
