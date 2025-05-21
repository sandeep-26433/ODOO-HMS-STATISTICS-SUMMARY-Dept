from odoo import models, fields

class AppointmentStatisticsLine(models.TransientModel):
    _name = 'appointment.statistics.line'
    _description = 'Appointment Statistics Line'

    wizard_id = fields.Many2one('appointment.statistics.wizard', string='Wizard')
    date = fields.Date(string='Date')
    male_count = fields.Integer(string='Male')
    female_count = fields.Integer(string='Female')
    others_count = fields.Integer(string='Others')
    total_count = fields.Integer(string='Total')
    new_patient_count = fields.Integer(string='New Patients')
    old_patient_count = fields.Integer(string='Old Patients')

    age_0_16_count = fields.Integer(string='Age 0-16')
    age_17_50_count = fields.Integer(string='Age 17-50')
    age_51_plus_count = fields.Integer(string='Age 51+')
    
    

    
    