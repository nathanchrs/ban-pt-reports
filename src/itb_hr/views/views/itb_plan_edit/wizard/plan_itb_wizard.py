from odoo import models, fields, api, exceptions
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive, GoogleDriveFile, GoogleDriveFileList
import os
import argparse

class plan_itb_wizard(models.TransientModel):
    _name = 'itb.plan_itb_wizard'

    @api.multi
    def _get_years(self):
        tahun=[]
        plan_int = self.env['itb.plan_int'].search([])
        year = sorted(set(plan_int.mapped('year')))
        for x in year: 
            output = ({x,x})
            tahun.append (output)
        return tahun

    year = fields.Selection('_get_years', string='Year')

    #year = fields.Selection(compute=_get_years, string='Year')

    def kirim_file(self):
        PARENT_ID = "LONG_FOLDER_ID_STRING"

        # Parse the passed arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("files", help="List files to be uploaded.", nargs="+")

        # Define the credentials folder
        home_dir = os.path.expanduser("~")
        credential_dir = os.path.join(home_dir, ".credentials")
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, "pydrive-credentials.json")

        # Start authentication
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(credential_path)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.CommandLineAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(credential_path)
        drive = GoogleDrive(gauth)

        # Upload the files
        for f in parser.parse_args().files:
            new_file = drive.CreateFile({"parents": [{"id": PARENT_ID}], "mimeType":"text/plain"})
            new_file.SetContentFile(f)
            new_file.Upload()

    @api.multi
    def set_plan_itb(self):
        thn = datetime.now()
        yr = thn.year + 1
        #plan = self.env['itb.plan'].search([('year', '=', yr)])
        #if plan:
        #    for rec in plan:
        #        itb.plan.unlink({'name':rec.name}
        #        )
        for plan_int in self:
            plan_int = self.env['itb.plan_int'].search([('year', '=', yr)])
            if plan_int:
                for x in plan_int:
                    if x.name:
                        itb.plan.create({
                            'name': x.name,
                            'year' : x.year,
                            'budget' : x.budget,
                            'percent_budget' : x.percent_budget,
                            'percent_performance' : x.percent_performance,
                            'state' : x.state,
                            #'plan_line_ids' : x.plan_line_ids,
                            #'target_ids' : x.target_ids,
                            #'spending_ids' : x.spending_ids
                            })
                    for y in x.plan_line_ids:
                        plan_line = self.env['itb.plan_line_int'].search([('plan_line_ids.name', '=', y.plan_line_ids)])
                        for pl in plan_line:
                            if pl.name:
                                itb.plan_line.create({
                                    'name' : pl.name,
                                    'code' : pl.code,
                                    'barang' : pl.barang,
                                    'jasa' : pl.jasa,
                                    'modal' : pl.modal,
                                    'pegawai' : pl.pegawai,
                                    'budget' : pl.budget,
                                    'percent_budget' : pl.percent_budget,
                                    'percent_performance' : pl.percent_performance,
                                    'program_id' : pl.program_id,
                                    'activity_id' : pl.activity_id,
                                    'subactivity_id' : pl.subactivity_id,
                                    'unit_id' : x.unit_id
                                    #'plan_id' : pl.plan_int_id,
                                    #'target_ids' : pl.target_ids,
                                    #'spending_ids' : pl.spending_ids
                                })
                    for w in x.target_ids:
                        target = self.env['itb.plan_target_int'].search([('target_ids.plan_int_id', '=', w.target_ids)])
                        for tg in target:
                            if tg.name:
                                itb.plan_target.create({
                                    'name' : tg.name,
                                    'standard' : tg.standard,
                                    'plan' : tg.plan,
                                    'actual' : tg.actual,
                                    'percent_performance' : tg.percent_performance#,
                                    #'plan_line_id' : tg.plan_line_id,
                                    #'indicator_id' : tg.indicator_id,
                                    #'plan_int_id' : tg.plan_int_id
                                })
                    for s in x.spending_ids:
                        spend = self.env['itb.plan_spending_int'].search([('spending_ids.plan_int_id','=',s.spending_ids)])
                        for sp in spend:
                            if sp.name:
                                itb.plan_spending.create({
                                    'name' : sp.name,
                                    'code' : sp.code,
                                    'month' : sp.month,
                                    'day' : sp.day,
                                    'standard' : sp.standard,
                                    'price' : sp.price,
                                    'volume' : sp.volume,
                                    'total' : sp.total,
                                    'used' : sp.used,
                                    'available' : sp.available,
                                    'paid' : sp.paid,
                                    'percent_budget' : sp.percent_budget,
                                    'type' : sp.type,
                                    'source' : sp.source,
                                    'actual_ids' : sp.actual_ids,
                                    'price_id' : sp.price_id,
                                    #'plan_id' : sp.plan_id,
                                    #'plan_line_id' : sp.plan_line_id,
                                    #'allocation_int_ids' : sp.allocation_int_ids
                                })