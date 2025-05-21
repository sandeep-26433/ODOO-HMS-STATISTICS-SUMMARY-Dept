from odoo import models, fields, api

class PurchaseManagementReport(models.AbstractModel):
    _name = 'report.pharmacy.purchase_report_template'
    _description = 'Purchase Management Report'

    def _get_report_values(self, docids, data=None):
        purchase_records = self.env['purchase.management'].browse(docids)
        company = self.env.company

        ReportModel = self.env['report.purchase.management']
        ReportLineModel = self.env['report.purchase.management.line']

        report_ids = []

        for record in purchase_records:
            report = ReportModel.create({
                'invoice_number': record.invoice_number,
                'vendor_name': record.vendor_id.name,
                'purchase_date': record.purchase_date,
                'overall_total': record.overall_total,
            })

            line_ids = []
            for line in record.line_ids:
                line_ids.append((0, 0, {
                    'report_id': report.id,
                    'product_name': line.product_id.name,
                    'quantity': line.quantity,
                    'cost': line.cost,
                    'lot_number': line.lot_number,
                    'expiry_date': line.expiry_date,
                    'total': line.total,
                }))

            report.write({'line_ids': line_ids})
            report_ids.append(report.id)

        return {
            'doc_ids': report_ids,
            'doc_model': 'report.purchase.management',
            'docs': ReportModel.browse(report_ids),
            'company': company,
            'company_logo': company.logo.decode('utf-8') if company.logo else False,
        }
