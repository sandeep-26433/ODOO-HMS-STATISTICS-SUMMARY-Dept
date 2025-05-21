from odoo import api, fields, models, _

class Vendors(models.Model):
    _name = "vendors"
    _description = "Vendors"

    patient_id = fields.Many2one(
        'res.partner',
        string="Vendor",
        required=False,  # Optional to allow for creation of new vendor
        help="Select existing vendor or create a new one via popup.",
    )
    name = fields.Char(string="Vendor Name", required=True)
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    gst_number = fields.Char(string="GST Number")

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id:
            self.name = self.patient_id.name or self.name  # Ensure name is populated from partner
            self.phone = self.patient_id.phone or self.phone
            self.email = self.patient_id.email or self.email
            self.address = self.patient_id.street or self.address
            self.gst_number = self.patient_id.vat or self.gst_number

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = vals.get('patient_id') and self.env['res.partner'].browse(vals['patient_id']).name

        # If the vendor (patient_id) doesn't exist, create a new partner
        if not vals.get('patient_id'):
            partner_vals = {
                'name': vals.get('name'),
                'phone': vals.get('phone'),
                'email': vals.get('email'),
                'street': vals.get('address'),
                'vat': vals.get('gst_number'),
                'is_company': True,  # You can adjust this based on your requirements
            }
            partner = self.env['res.partner'].create(partner_vals)
            vals['patient_id'] = partner.id  # Link the newly created partner

        res = super(Vendors, self).create(vals)

        # Ensure details are saved in res.partner after vendor creation
        if res.patient_id:
            res.patient_id.write({
                'phone': res.phone or '',
                'email': res.email or '',
                'street': res.address or '',
                'vat': res.gst_number or '',
            })

        return res

    def write(self, vals):
        res = super(Vendors, self).write(vals)
        for rec in self:
            if rec.patient_id:
                updated_vals = {}
                if 'phone' in vals:
                    updated_vals['phone'] = vals['phone']
                if 'email' in vals:
                    updated_vals['email'] = vals['email']
                if 'address' in vals:
                    updated_vals['street'] = vals['address']
                if 'gst_number' in vals:
                    updated_vals['vat'] = vals['gst_number']

                if updated_vals:
                    rec.patient_id.write(updated_vals)  # Update the res.partner record
        return res
    
    
