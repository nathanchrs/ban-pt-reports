from odoo import api, fields, models, tools, exceptions


class MembershipReport(models.Model):
    _name = "itb.hr_report_membership"
    _description = "Membership Organisasi Dosen"
    _auto = False

    employee_id =  fields.Many2one('hr.employee', string='Employee id', readonly=True)
    name = fields.Char(string='Name', readonly=True)
    organization = fields.Char(string='Organization', readonly=True)
    year = fields.Char(string='Year', readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'itb_hr_report_membership')
        self._cr.execute("""
            CREATE OR REPLACE VIEW itb_hr_report_membership AS (
                SELECT
                    min(a.id) as id,
                    a.employee_id,
                    b.name_related as name,
                    a.name as organization,
                    string_agg(cast(date_part('year',a.start) as text), ', ') AS year
                FROM 
                    itb_hr_membership a, hr_employee b
                WHERE 
                    b.id=a.employee_id
                GROUP BY 
                    a.employee_id,b.name_related,a.name
            )
        """)