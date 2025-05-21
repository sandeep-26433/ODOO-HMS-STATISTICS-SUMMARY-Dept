from odoo import models, fields, api
from datetime import timedelta
import base64
import io
import xlsxwriter

class AppointmentStatisticsWizard(models.TransientModel):
    _name = 'appointment.statistics.wizard'
    _description = 'Appointment Statistics Wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)

    line_ids = fields.One2many('appointment.statistics.line', 'wizard_id', string='Date-wise Statistics')
    total_count = fields.Integer(string='Total Appointments', readonly=True)
    total_new_patients = fields.Integer(string='Total New Patients', readonly=True)
    total_old_patients = fields.Integer(string='Total Old Patients', readonly=True)
    export_file = fields.Binary(string='Export File', readonly=True)
    export_filename = fields.Char(string='Filename', readonly=True)
    
    # Add age group totals
    total_age_0_16 = fields.Integer(string='Total Age 0-16', readonly=True)
    total_age_17_50 = fields.Integer(string='Total Age 17-50', readonly=True)
    total_age_51_plus = fields.Integer(string='Total Age 51+', readonly=True)

    # Add gender totals
    total_male = fields.Integer(string='Total Male', readonly=True)
    total_female = fields.Integer(string='Total Female', readonly=True)
    total_others = fields.Integer(string='Total Others', readonly=True)

    # Add department statistics
    total_kayachikitsa = fields.Integer(string='Total KAYACHIKITSA', readonly=True)
    total_panchakarma = fields.Integer(string='Total PANCHAKARMA', readonly=True)
    total_streerogam_prasutitantra = fields.Integer(string='Total STREEROGAM & PRASUTITANTRA', readonly=True)
    total_kaumarabrityam = fields.Integer(string='Total KAUMARABRITYAM', readonly=True)
    total_shalyam = fields.Integer(string='Total SHALAYAM', readonly=True)
    total_shalakyam = fields.Integer(string='Total SHALAKYAM', readonly=True)
    total_swastavrittan = fields.Integer(string='Total SWASTAVRITTAN', readonly=True)
    total_emergency = fields.Integer(string='Total EMERGENCY', readonly=True)
    total_ip = fields.Integer(string='Total IP', readonly=True)
    total_counter_sales = fields.Integer(string='Total COUNTER SALES', readonly=True)

    def calculate_statistics(self):
        self.line_ids.unlink()  # Clear previous results

        total_overall = 0
        total_new_patients = 0  # To store total new patients
        total_old_patients = 0  # To store total old patients
        total_age_0_16 = 0
        total_age_17_50 = 0
        total_age_51_plus = 0
        total_male = 0
        total_female = 0
        total_others = 0
        department_counts = {
            'kayachikitsa': 0,
            'panchakarma': 0,
            'streerogam_prasutitantra': 0,
            'kaumarabrityam': 0,
            'shalyam': 0,
            'shalakyam': 0,
            'swastavrittan': 0,
            'emergency': 0,
            'ip': 0,
            'counter_sales': 0
        }

        date_cursor = self.from_date
        while date_cursor <= self.to_date:
            domain = [('appointment_date', '=', date_cursor)]

            # Count patients by age groups
            age_0_16_count = self.env['appointment.booking'].search_count(domain + [('age', '>=', 0), ('age', '<=', 16)])
            age_17_50_count = self.env['appointment.booking'].search_count(domain + [('age', '>', 16), ('age', '<=', 50)])
            age_51_plus_count = self.env['appointment.booking'].search_count(domain + [('age', '>', 50)])

            # Count other statistics
            new_patient_count = self.env['appointment.booking'].search_count(domain + [('patient_type', '=', 'new')])
            old_patient_count = self.env['appointment.booking'].search_count(domain + [('patient_type', '=', 'old')])
            male_count = self.env['appointment.booking'].search_count(domain + [('gender', '=', 'male')])
            female_count = self.env['appointment.booking'].search_count(domain + [('gender', '=', 'female')])
            others_count = self.env['appointment.booking'].search_count(domain + [('gender', '=', 'others')])

            # Count by departments
            for department in department_counts.keys():
                department_count = self.env['appointment.booking'].search_count(domain + [('department', '=', department)])
                department_counts[department] += department_count

            total_for_day = male_count + female_count + others_count
            total_overall += total_for_day
            total_new_patients += new_patient_count
            total_old_patients += old_patient_count
            total_age_0_16 += age_0_16_count
            total_age_17_50 += age_17_50_count
            total_age_51_plus += age_51_plus_count
            total_male += male_count
            total_female += female_count
            total_others += others_count

            self.env['appointment.statistics.line'].create({
                'wizard_id': self.id,
                'date': date_cursor,
                'male_count': male_count,
                'female_count': female_count,
                'others_count': others_count,
                'total_count': total_for_day,
                'new_patient_count': new_patient_count,
                'old_patient_count': old_patient_count,
                'age_0_16_count': age_0_16_count,
                'age_17_50_count': age_17_50_count,
                'age_51_plus_count': age_51_plus_count
            })

            date_cursor += timedelta(days=1)

        # Store the totals in the wizard
        self.total_count = total_overall
        self.total_new_patients = total_new_patients
        self.total_old_patients = total_old_patients
        self.total_age_0_16 = total_age_0_16
        self.total_age_17_50 = total_age_17_50
        self.total_age_51_plus = total_age_51_plus
        self.total_male = total_male
        self.total_female = total_female
        self.total_others = total_others

        # Store department statistics
        self.total_kayachikitsa = department_counts['kayachikitsa']
        self.total_panchakarma = department_counts['panchakarma']
        self.total_streerogam_prasutitantra = department_counts['streerogam_prasutitantra']
        self.total_kaumarabrityam = department_counts['kaumarabrityam']
        self.total_shalyam = department_counts['shalyam']
        self.total_shalakyam = department_counts['shalakyam']
        self.total_swastavrittan = department_counts['swastavrittan']
        self.total_emergency = department_counts['emergency']
        self.total_ip = department_counts['ip']
        self.total_counter_sales = department_counts['counter_sales']

        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment Statistics',
            'res_model': 'appointment.statistics.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def export_excel(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        # Create the first worksheet for the detailed statistics
        worksheet = workbook.add_worksheet('Statistics')

        # Define bold format for headers
        bold_format = workbook.add_format({'bold': True})

        # Adjust column widths
        worksheet.set_column(0, 0, 15)  # Date column
        worksheet.set_column(1, 4, 10)  # Numeric columns

        # Write headers in bold
        headers = ['Date', 'Male', 'Female', 'Others', 'New Patients', 'Old Patients', 
                   'Age 0-16', 'Age 17-50', 'Age 51+', 'Total']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, bold_format)

        # Write data rows (date as plain string)
        row_num = 1
        for line in self.line_ids:
            worksheet.write(row_num, 0, str(line.date))  # date as string
            worksheet.write(row_num, 1, line.male_count)
            worksheet.write(row_num, 2, line.female_count)
            worksheet.write(row_num, 3, line.others_count)
            worksheet.write(row_num, 9, line.total_count)
            worksheet.write(row_num, 4, line.new_patient_count)
            worksheet.write(row_num, 5, line.old_patient_count)
            worksheet.write(row_num, 6, line.age_0_16_count)
            worksheet.write(row_num, 7, line.age_17_50_count)
            worksheet.write(row_num, 8, line.age_51_plus_count)
            row_num += 1

        # Add overall total at the bottom, in bold
        row_num += 1
        worksheet.write(row_num, 0, 'Overall Total', bold_format)
        worksheet.write(row_num, 9, self.total_count, bold_format)
        worksheet.write(row_num, 4, self.total_new_patients)  # Total New Patients
        worksheet.write(row_num, 5, self.total_old_patients)  # Total Old Patients
        worksheet.write(row_num, 6, self.total_age_0_16)
        worksheet.write(row_num, 7, self.total_age_17_50)
        worksheet.write(row_num, 8, self.total_age_51_plus)

        # Create a new worksheet for the department statistics
        department_worksheet = workbook.add_worksheet('Department')

        # Set the column width and row height for the department sheet
        department_worksheet.set_column('A:A', 30)  # Set the width of the 'A' column
        department_worksheet.set_column('B:B', 15)  # Set the width of the 'B' column

        # Write headers for department statistics
        department_worksheet.write('A1', 'Department', bold_format)
        department_worksheet.write('B1', 'Count', bold_format)

        # Write department data
        departments = [
            ('KAYACHIKITSA', self.total_kayachikitsa),
            ('PANCHAKARMA', self.total_panchakarma),
            ('STREEROGAM & PRASUTITANTRA', self.total_streerogam_prasutitantra),
            ('KAUMARABRITYAM', self.total_kaumarabrityam),
            ('SHALAYAM', self.total_shalyam),
            ('SHALAKYAM', self.total_shalakyam),
            ('SWASTAVRITTAN', self.total_swastavrittan),
            ('EMERGENCY', self.total_emergency),
            ('IP', self.total_ip),
            ('COUNTER SALES', self.total_counter_sales)
        ]

        # Add Date Range to the department sheet
        department_worksheet.write('A2', f"Date Range: {self.from_date} to {self.to_date}", bold_format)

        row = 3
        for department, count in departments:
            department_worksheet.write(row, 0, department)
            department_worksheet.write(row, 1, count)
            row += 1

        # Create a new worksheet for the summary
        summary_worksheet = workbook.add_worksheet('Summary')

        # Set the column width and row height for the summary sheet
        summary_worksheet.set_column('A:A', 20)  # Set the width of the 'A' column
        summary_worksheet.set_column('B:B', 20)  # Set the width of the 'B' column
        summary_worksheet.set_row(0, 30)  # Increase the height of the first row for title

        # Define custom format for the "Total Appointments" cell (Large size, red color)
        big_red_format = workbook.add_format({'bold': True, 'font_size': 16, 'color': 'red'})

        # Set up summary headers
        summary_title_format = workbook.add_format({'bold': True, 'font_size': 16})

        summary_worksheet.write('A1', 'Summary Report', summary_title_format)
        summary_worksheet.write('A3', 'Date Range:', bold_format)
        summary_worksheet.write('A4', 'Total Appointments', bold_format)
        summary_worksheet.write('A5', 'Total New Patients', bold_format)
        summary_worksheet.write('A6', 'Total Old Patients', bold_format)
        summary_worksheet.write('A7', 'Age 0-16 Count', bold_format)
        summary_worksheet.write('A8', 'Age 17-50 Count', bold_format)
        summary_worksheet.write('A9', 'Age 51+ Count', bold_format)
        summary_worksheet.write('A10', 'Total Male Count', bold_format)
        summary_worksheet.write('A11', 'Total Female Count', bold_format)
        summary_worksheet.write('A12', 'Total Others Count', bold_format)

        # Write summary data
        summary_worksheet.write('B3', f'{self.from_date} to {self.to_date}', bold_format)
        summary_worksheet.write('B4', self.total_count, big_red_format)  # Total Appointments in big red
        summary_worksheet.write('B5', self.total_new_patients)
        summary_worksheet.write('B6', self.total_old_patients)
        summary_worksheet.write('B7', self.total_age_0_16)
        summary_worksheet.write('B8', self.total_age_17_50)
        summary_worksheet.write('B9', self.total_age_51_plus)
        summary_worksheet.write('B10', self.total_male)
        summary_worksheet.write('B11', self.total_female)
        summary_worksheet.write('B12', self.total_others)

        # Close the workbook and save the file
        workbook.close()
        output.seek(0)

        # Encode the file
        b64_content = base64.b64encode(output.read())
        filename = f'appointment_statistics_{self.from_date}_to_{self.to_date}.xlsx'

        # Save file and filename on the record
        self.write({
            'export_file': b64_content,
            'export_filename': filename
        })

        # Return download action
        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/{self._name}/{self.id}/export_file/{filename}?download=true",
            'target': 'self',
        }

