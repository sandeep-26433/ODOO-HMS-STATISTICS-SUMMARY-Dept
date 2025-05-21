from odoo import models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def action_print_custom_pos_invoice(self):
     return {
        'type': 'ir.actions.report',
        'report_type': 'qweb-pdf',
        'report_name': 'dr_home.report_pos_custom_summary',  # your QWeb template ID
        'report_file': 'dr_home.report_pos_custom_summary',
        'name': 'POS Custom Invoice',
        'res_model': 'pos.order',
        'res_id': self.id,
    }
   
