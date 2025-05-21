from odoo import models, fields, api
class ReportPurchaseManagementLine(models.TransientModel):
    _name = 'report.purchase.management.line'
    _description = 'Purchase Report Lines'

    report_id = fields.Many2one('report.purchase.management', string="Report", ondelete='cascade')
    product_name = fields.Char("Product")
    quantity = fields.Float("Quantity")
    cost = fields.Float("Cost")
    lot_number = fields.Char("Lot Number")
    expiry_date = fields.Date("Expiry Date")
    total = fields.Float("Total")
