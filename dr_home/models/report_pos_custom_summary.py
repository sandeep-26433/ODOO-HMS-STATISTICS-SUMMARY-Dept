from odoo import models
# from odoo.addons.base.models.ir_qweb import format_amount_to_text as amount_to_text


class POSCustomSummaryReport(models.AbstractModel):
    _name = 'report.dr_home.report_pos_custom_summary'
    _description = 'Custom POS Order Summary Report'

    def _get_report_values(self, docids, data=None):
        pos_orders = self.env['pos.order'].browse(docids)
        report_model = self.env['report.pos.custom.summary']
        company = self.env.company
        
        records = []

        for order in pos_orders:
            appointment = self.env['doctor.appointments'].search(
                [('patient_id', '=', order.partner_id.id)],
                order='appointment_date desc',
                limit=1
            )

            # 🧾 Fallback values if no appointment found
            age = appointment.age if appointment else 0
            gender = appointment.gender if appointment else ''
            consultation_doctor=appointment.consultation_doctor.name if appointment else ''
            reference_id = appointment.reference_id if appointment else ''
            invoice_number = order.account_move.name if order.account_move else ''
            amount_due = order.amount_total - order.amount_paid + order.amount_return
        

           
          



            summary = report_model.create({
                'order_id': order.id,
                'customer': order.partner_id.name or "Guest",
                'order_date': order.date_order,
                'total_amount': order.amount_total,
                'patient_age': age,
                'gender': gender,
                'patient_id': reference_id,
                'invoice_number': invoice_number, 
                 'amount_due':amount_due,
                 'consultation_doctor':consultation_doctor
              
            })

            for line in order.lines:
                self.env['report.pos.custom.line'].create({
                    'report_id': summary.id,
                    'product_name': line.full_product_name or line.product_id.name,
                    'qty': line.qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal_incl,
                })

            records.append(summary.id)

        return {
            'doc_ids': records,
            'doc_model': 'report.pos.custom.summary',
            'docs': report_model.browse(records),
            'company': company,
            'company_logo': company.logo.decode('utf-8') if company.logo else False,
        }
    