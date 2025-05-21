from odoo import api, fields, models

class PurchaseManagementLine(models.Model):
    _name = 'purchase.management.line'
    _description = 'Purchase Management Line'

    purchase_management_id = fields.Many2one('purchase.management', string='Vendor Reference', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    cost = fields.Float(string='Cost', required=True)
    lot_number = fields.Char(string='Lot Number')
    expiry_date = fields.Date(string='Expiry Date')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            lot = self.env['stock.lot'].search([('product_id', '=', self.product_id.id)], limit=1)
            if lot:
                self.lot_number = lot.name


    @api.depends('quantity', 'cost')
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.cost
