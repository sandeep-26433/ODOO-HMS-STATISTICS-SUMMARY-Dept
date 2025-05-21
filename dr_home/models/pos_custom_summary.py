from odoo import models, fields

class ReportPOSCustomSummary(models.TransientModel):
    _name = 'report.pos.custom.summary'
    _description = 'POS Custom Summary'

    order_id = fields.Many2one('pos.order', string='POS Order')
    customer = fields.Char(string='Customer')
    order_date = fields.Datetime(string='Order Date')
    total_amount = fields.Float(string='Total')
    line_ids = fields.One2many('report.pos.custom.line', 'report_id', string='POS Lines')
    patient_age = fields.Integer(string="Age")
    gender = gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ])
   
    patient_id = fields.Char(string="UHID")
    invoice_number = fields.Char(string="Invoice Number")
    currency_id = fields.Many2one('res.currency', string="Currency")
    amount_due = fields.Monetary(string="Amount Due", currency_field='currency_id')
    consultation_doctor=fields.Char("Doctor Name")






class ReportPOSCustomLine(models.TransientModel):
    _name = 'report.pos.custom.line'
    _description = 'POS Custom Line'

    report_id = fields.Many2one('report.pos.custom.summary', string='Report')
    product_name = fields.Char(string='Product')
    qty = fields.Float(string='Qty')
    price_unit = fields.Float(string='Unit Price')
    price_subtotal = fields.Float(string='Subtotal')
