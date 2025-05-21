from odoo import models, fields, api
class ReportPurchaseManagement(models.TransientModel):
    _name = 'report.purchase.management'
    _description = 'Purchase Report Data'

    invoice_number = fields.Char("Invoice Number")
    vendor_name = fields.Char("Vendor")
    purchase_date = fields.Date("Purchase Date")
    overall_total = fields.Float("Overall Total")

    line_ids = fields.One2many('report.purchase.management.line', 'report_id', string='Product Lines')