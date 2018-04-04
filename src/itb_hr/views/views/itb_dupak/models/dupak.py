from odoo import models, fields, api, exceptions
from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from datetime import datetime


class Dupak(models.Model):
    _name = 'itb.dupak'
    _rec_name = 'employee_id'
    
    @api.model
    def _get_eligible_employee(self):
        onprocess = self.search([('state','!=','done')]).mapped('employee_id.id')
        return [('employment_type','=','pns'),('is_faculty','=',True),('id','not in',onprocess)]
    
    '''
    @api.model
    def _get_dupak_start(self):
        last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_jabatan.start:
            return last_jabatan.start
        else:
            return self.employee_id.pns_start

    @api.model
    def _get_dupak_jabatan(self):
        last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_jabatan.jabatan:
            return (last_jabatan.jabatan + ' tmt ' + datetime.strptime(last_jabatan.start, '%Y-%m-%d').strftime('%d %B %Y'))
        else:
            return ('- tmt ' + datetime.strptime(self.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y'))
            

    @api.model
    def _get_dupak_pangkat(self):    
        last_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_pangkat.pangkat:
            return (last_pangkat.pangkat + ' tmt ' + datetime.strptime(last_pangkat.start, '%Y-%m-%d').strftime('%d %B %Y'))
        else:
            return ('- tmt ' + datetime.strptime(self.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y'))
    
    @api.model
    def _get_next_pangkat(self):
        last_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_pangkat.pangkat_id.sequence:
            return (self.env['itb.hr_pangkat_type'].search([('sequence','>',last_pangkat.pangkat_id.sequence)],limit=1,order='sequence'))
        else:
            return (self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence'))

    @api.model
    def _get_next_jabatan(self):
        last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_jabatan.jabatan_id.sequence:
            return (self.env['itb.hr_jabatan_type'].search([('sequence','>',last_jabatan.jabatan_id.sequence)],limit=1,order='sequence'))
        else:
            return (self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence'))

    @api.model
    def _get_target_jabatan(self):
        last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','>',last_jabatan.jabatan_id.sequence)],limit=1,order='sequence')
        if next_jabatan:
            return next_jabatan.id
        else:
            next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')
            return next_jabatan.id

    @api.model
    def _get_target_pangkat(self):
        #import pdb;pdb.set_trace()
        last_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
        if last_pangkat:
            next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','>',last_pangkat.pangkat_id.sequence)],limit=1,order='sequence')
            if next_pangkat:
                return next_pangkat.id
            else:
                return last_pangkat.id
        else:
            next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')
            #import pdb;pdb.set_trace()
            return next_pangkat.id
    '''

    pangkat = fields.Char(compute='_get_employee_info',store=True)
    jabatan = fields.Char(compute='_get_employee_info',store=True)
    next_pangkat = fields.Char(compute='_get_employee_info',store=True)
    next_jabatan = fields.Char(compute='_get_employee_info',store=True)
    education = fields.Char(compute='_get_employee_info',store=True)    
    period = fields.Char(compute='_get_employee_info',store=True)
    start = fields.Date()
    finish = fields.Date(default=fields.Date.today())
    total_score = fields.Float(compute='_get_total_score', store=True)
    final_score = fields.Float(compute='_get_total_score', store=True)
    education_score = fields.Float(compute='_get_total_score', store=True)
    pendidikan_score = fields.Float(compute='_get_total_score', store=True)
    penelitian_score = fields.Float(compute='_get_total_score', store=True)
    pengabdian_score = fields.Float(compute='_get_total_score', store=True)
    penunjang_score = fields.Float(compute='_get_total_score', store=True)
    education_final = fields.Float(default=0)
    pendidikan_final = fields.Float(default=0)
    penelitian_final = fields.Float(default=0)
    pengabdian_final = fields.Float(default=0)
    penunjang_final = fields.Float(default=0)
    total_score_final = fields.Float(compute='_get_total_score_final', store=True)
    #final_score_final = fields.Float(compute='_get_total_score', store=True)
    school_file = fields.Binary()
    university_file = fields.Binary()
    dikti_file = fields.Binary()
    last_period = fields.Char(related='last_id.period')
    last_score = fields.Float(related='last_id.final_score', string='Last score')
    state = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('review','Reviewed'),('itb','ITB'),('dikti','Dikti'),('done','Done')], 'Status', default='draft', required=True, copy=False)
    reference = fields.Char()
    signed_by = fields.Char()
    date_confirm = fields.Date()
    date_itb = fields.Date()
    date_dikti = fields.Date()
    date_decision = fields.Date()
    date_start =  fields.Date()
    last_id =  fields.Many2one('itb.dupak', string='Previous DUPAK')
    employee_id =  fields.Many2one('hr.employee', string='Name', domain=_get_eligible_employee)
    pangkat_id =  fields.Many2one('itb.hr_pangkat_type', string='Target Pangkat')
    jabatan_id =  fields.Many2one('itb.hr_jabatan_type', string='Target Jabatan')
    line_ids = fields.One2many('itb.dupak_line','dupak_id',string='Detail')

    
    @api.multi
    #@api.onchange('employee_id')
    #@api.depends('employee_id')
    def _get_dupak_start(self):
        if self.employee_id:
            last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
            last_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
            next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','>',last_jabatan.jabatan_id.sequence)],limit=1,order='sequence')
            next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','>',last_pangkat.pangkat_id.sequence)],limit=1,order='sequence')

            if last_jabatan.start:
                self.start = last_jabatan.start
            else:
                self.start = self.employee_id.pns_start

            if last_jabatan.jabatan:
                self.jabatan = last_jabatan.jabatan + ' tmt ' + datetime.strptime(last_jabatan.start, '%Y-%m-%d').strftime('%d %B %Y')
            else:
                if self.employee_id.pns_start:
                    self.jabatan = '- tmt ' + datetime.strptime(self.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y')
                else:
                    if self.employee_id.cpns_start:
                        self.jabatan = '- tmt ' + datetime.strptime(self.employee_id.cpns_start, '%Y-%m-%d').strftime('%d %B %Y')
            
            if last_pangkat.pangkat:
                self.pangkat = last_pangkat.pangkat + ' tmt ' + datetime.strptime(last_pangkat.start, '%Y-%m-%d').strftime('%d %B %Y')
            else:
                self.pangkat = '- tmt ' + datetime.strptime(self.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y')
            
            if last_pangkat.pangkat_id.sequence:
                self.next_pangkat = next_pangkat
            else:
                self.next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')

            if last_jabatan.jabatan_id.sequence:
                self.next_jabatan = next_jabatan
            else:
                self.next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')

            if last_pangkat:
                if next_pangkat:
                    self.pangkat_id =  next_pangkat.id
                else:
                    self.pangkat_id =  last_pangkat.id
            else:
                next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')
                #import pdb;pdb.set_trace()
                self.pangkat_id =  next_pangkat.id

            if last_jabatan:
                if next_jabatan:
                    self.jabatan_id =  next_jabatan.id
                else:
                    self.jabatan_id =  last_jabatan.id
            else:
                next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')
                #import pdb;pdb.set_trace()
                self.jabatan_id =  next_jabatan.id    
    
    @api.onchange('employee_id')
    @api.depends('employee_id')
    def _get_employee_info(self):
        for dupak in self:
            if dupak.employee_id:
                l_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',dupak.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
                l_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',dupak.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
                n_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','>',l_jabatan.jabatan_id.sequence)],limit=1,order='sequence')
                n_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','>',l_pangkat.pangkat_id.sequence)],limit=1,order='sequence')
                n_pangkat2 = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')
                n_jabatan2 = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')

                if l_jabatan.start:
                    dupak.start = l_jabatan.start
                else:
                    if dupak.employee_id.pns_start:
                        dupak.start = dupak.employee_id.pns_start
                    elif dupak.employee_id.cpns_start:
                        dupak.start = dupak.employee_id.cpns_start


                if l_jabatan.jabatan:
                    dupak.jabatan = l_jabatan.jabatan + ' tmt ' + datetime.strptime(l_jabatan.start, '%Y-%m-%d').strftime('%d %B %Y')
                else:
                    if dupak.employee_id.pns_start:
                        dupak.jabatan = '- tmt ' + datetime.strptime(dupak.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y')
                    else:
                        if dupak.employee_id.cpns_start:
                            dupak.jabatan = '- tmt ' + datetime.strptime(dupak.employee_id.cpns_start, '%Y-%m-%d').strftime('%d %B %Y')
                
                if l_pangkat.pangkat:
                    dupak.pangkat = l_pangkat.pangkat + ' tmt ' + datetime.strptime(l_pangkat.start, '%Y-%m-%d').strftime('%d %B %Y')
                else:
                    dupak.pangkat = '- tmt ' + datetime.strptime(dupak.employee_id.pns_start, '%Y-%m-%d').strftime('%d %B %Y')
                
                if l_pangkat.pangkat_id.sequence:
                    dupak.next_pangkat = n_pangkat.name
                else:
                    xxx = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')
                    dupak.next_pangkat = xxx.name

                if l_jabatan.jabatan_id.sequence:
                    dupak.next_jabatan = n_jabatan.name
                else:
                    xxx = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')
                    dupak.next_jabatan = xxx.name

                #raise models.ValidationError(str(l_pangkat) + '||' + str(n_pangkat) + '#' +  str(l_jabatan) + '||' + str(n_jabatan))
                if l_pangkat:
                    if n_pangkat:
                        dupak.pangkat_id =  n_pangkat.id
                    else:
                        dupak.pangkat_id =  l_pangkat.id
                else:
                    n_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','=',30)],limit=1,order='sequence')
                    dupak.pangkat_id =  n_pangkat.id

                if l_jabatan:
                    if n_jabatan:
                        dupak.jabatan_id =  n_jabatan.id
                    else:
                        dupak.jabatan_id =  l_jabatan.id
                else:
                    n_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','=',10)],limit=1,order='sequence')
                    dupak.jabatan_id =  n_jabatan.id 

                #self._get_dupak_start()
                #last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',dupak.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
                #dupak.start = last_jabatan.start
                #dupak.jabatan = self.jabatan #last_jabatan.jabatan + ' tmt ' + datetime.strptime(last_jabatan.start, '%Y-%m-%d').strftime('%d %B %Y')
                #last_pangkat = self.env['itb.hr_pangkat'].search([('employee_id.id','=',dupak.employee_id.id),('finish','=',False)],limit=1,order='start DESC')
                #dupak.pangkat = self.pangkat #last_pangkat.pangkat + ' tmt ' + datetime.strptime(last_pangkat.start, '%Y-%m-%d').strftime('%d %B %Y')
                last_education = self.env['itb.hr_education'].search([('employee_id.id','=',dupak.employee_id.id)],limit=1,order='finish DESC')
                dupak.education = last_education.degree
                start = datetime.strptime(dupak.start, '%Y-%m-%d')#datetime.strptime(dupak.employee_id.pns_start, '%Y-%m-%d')
                today = datetime.today()
                months = (today.year - start.year)*12 + today.month - start.month
                dupak.period = str(months/12) + ' tahun ' + str(months%12) + ' bulan'
                #next_jabatan = self.env['itb.hr_jabatan_type'].search([('sequence','>',last_jabatan.jabatan_id.sequence)],limit=1,order='sequence')
                #dupak.jabatan_id = self.jabatan_id #next_jabatan.id
                #dupak.next_jabatan = next_jabatan.name
                #next_pangkat = self.env['itb.hr_pangkat_type'].search([('sequence','>',last_pangkat.pangkat_id.sequence)],limit=1,order='sequence')
                #dupak.pangkat_id = self.pangkat_id# next_pangkat.id
                #Sdupak.next_pangkat = next_pangkat.name
                 


    #@api.depends('penelitian_final','pengabdian_final','penunjang_final','education_final','pendidikan_final')
    def _get_total_score_final(self):
        for dupak in self:
            dupak.total_score_final = dupak.education_final + dupak.pendidikan_final + dupak.penelitian_final + dupak.pengabdian_final + dupak.penunjang_final
    
    @api.multi
    def write(self, vals):
        if self.state == 'dikti':
            education = vals['education_final'] if 'education_final' in vals else self.education_final
            pendidikan = vals['pendidikan_final'] if 'pendidikan_final' in vals else self.pendidikan_final
            penelitian = vals['penelitian_final'] if 'penelitian_final' in vals else self.penelitian_final
            pengabdian = vals['pengabdian_final'] if 'pengabdian_final' in vals else self.pengabdian_final
            penunjang = vals['penunjang_final'] if 'penunjang_final' in vals else self.penunjang_final
            vals['total_score_final'] = education + pendidikan + penelitian + pengabdian + penunjang
        res = super(Dupak, self).write(vals)
        return res
    
    @api.depends('line_ids')
    def _get_total_score(self):
        #import pdb; pdb.set_trace()
        for dupak in self:
             
            education = dupak.line_ids.filtered(lambda x: x.code.startswith('I.'))
            if education:
                dupak.education_score = sum(education.mapped('score'))
            
            pendidikan = dupak.line_ids.filtered(lambda x: x.code.startswith('II.'))
            if pendidikan:
                dupak.pendidikan_score = sum(pendidikan.mapped('score'))

            penelitian = dupak.line_ids.filtered(lambda x: x.code.startswith('III.'))
            if penelitian:
                dupak.penelitian_score = sum(penelitian.mapped('score'))

            pengabdian = dupak.line_ids.filtered(lambda x: x.code.startswith('IV.'))
            if pengabdian:
                dupak.pengabdian_score = sum(pengabdian.mapped('score'))

            penunjang = dupak.line_ids.filtered(lambda x: x.code.startswith('V.'))
            if penunjang:
                dupak.penunjang_score = sum(penunjang.mapped('score'))

            dikti = dupak.line_ids.filtered(lambda x: x)

            dupak.total_score = dupak.education_score + dupak.pendidikan_score + dupak.penelitian_score + dupak.pengabdian_score + dupak.penunjang_score
            dupak.final_score = dupak.last_score + dupak.total_score
        


    # for now,every update simply remove dupak line with new line
    def update_dupak(self):
        result = []
        #get last jabatan
        last_jabatan = self.env['itb.hr_jabatan'].search([('employee_id.id','=',self.employee_id.id),('finish','=',False)])
        if last_jabatan.start == False:
            last_jabatan = self.env['itb.dupak'].search([('id','=',self.id)], order='id desc', limit=1)

        #get all standards
        standards = self.env['itb.dupak_standard'].search([])
        #get all semesters, useful to convert a day to particular semester
        semesters = self.env['itb.academic_semester'].search([])
        #get all publication, useful in many standards
        publications = self.env['itb.hr_publication_author'].search([('employee_id.id','=',self.employee_id.id),('publication_id.day','>=',last_jabatan.start),('publication_id.standard_id','!=',False)])
        #get all duty, useful in many standards
        duties = self.env['itb.hr_duty_employee'].search([('employee_id.id','=',self.employee_id.id),('standard_id','!=',False),'|',('start','>=',last_jabatan.start),('finish','>=',last_jabatan.start)])

        #standard I.A.A
        educations = self.env['itb.hr_education'].search([('employee_id.id','=',self.employee_id.id),('degree','in',['doctoral','graduate']),('finish','>=',last_jabatan.start)])
        
        if educations:
            for item in educations:
                code = 'I.A.1' if item.degree=='doctoral' else 'I.A.2'
                standard = standards.filtered(lambda r: r.code == code)
                period = datetime.strptime(item.finish, '%Y-%m-%d').strftime('%d %B %Y')
                name = item.school + ', ' + item.major + ', ' + period
                note = ''
                reference = 'itb.hr_education,' + str(item.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #standard I.A.B
        trainings = self.env['itb.hr_training'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start),('standard_id.code','=','I.A.B.2')])
        
        if trainings:
            for item in trainings:
                standard = item.standard_id
                code = standard.code
                period = datetime.strptime(item.start, '%Y-%m-%d').strftime('%d %B %Y') + ' - ' +  datetime.strptime(item.finish, '%Y-%m-%d').strftime('%d %B %Y')
                name = item.name
                note = ''
                reference = 'itb.hr_training,' + str(item.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #standard II.A
        teachings = self.env['itb.academic_instructor'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start)],order='semester')

        if teachings:
            jabatan = last_jabatan.jabatan_id.name
            cumsum = 0
            last_semester = ''
            i = 0
            overlimit = False

            for item in teachings:
                code = 'II.A'
                standard = standards.filtered(lambda r: r.code == code)
                period = item.semester
                name = item.course_id.name + ' (' + str(item.credit) + ' sks)'
                note = ''
                reference = 'itb.academic_instructor,' + str(item.id)
                volume = item.credit
                
                if i == 0:
                    last_semester = item.semester
                else:
                    if item.semester != last_semester:
                        cumsum = 0
                        overlimit = False

                cumsum = cumsum + volume

                if  not jabatan.strip().startswith('Asisten Ahli'):
                    if cumsum <= 10:
                        score_max = 1
                        score = volume * score_max
                    if cumsum >10 and cumsum <=12:
                        score_max = 0.5
                        after10 = cumsum - 10
                        score = (volume - after10) + (after10 * score_max)
                    if  cumsum > 12:
                        score_max = 0
                        if not overlimit:
                            if cumsum-volume <= 12:
                                score = (12-(cumsum-volume))*0.5    
                        else:
                            score = 0
                        overlimit = True    
                else:
                    if  cumsum <= 10:
                        score_max = 0.5
                        score = volume * score_max
                    if cumsum >10 and cumsum <=12:
                        score_max = 0.25
                        after10 = cumsum - 10
                        score = (volume - after10)*0.5 + (after10 * score_max)
                    if  cumsum > 12:
                        score_max = 0
                        if not overlimit:
                            if cumsum-volume <= 12:
                                score = (12-(cumsum-volume))*0.25    
                        else:
                            score = 0
                        overlimit = True

                last_semester = item.semester
                i = i + 1
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                result.append(output)


        #standard II.B, II.C, II.K, II.L,V.J for duties each semester
        duty_semester = ['II.B','II.C','II.K.1','II.K.2','V.J']
        duties_semester = duties.filtered(lambda x: x.standard_id.code in duty_semester) 

        if duties_semester:
            for item in duties_semester:
                standard = item.standard_id
                code = standard.code
                start = datetime.strptime(item.duty_id.start, '%Y-%m-%d')
                finish = datetime.strptime(item.duty_id.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.duty
                note = item.reference
                reference = 'itb.hr_duty,' + str(item.duty_id.id)
                today = datetime.today()
                
                if finish > today:
                    months = (today.year - start.year)*12 + today.month - start.month
                else:
                    months = (finish.year - start.year)*12 + finish.month - start.month
                
                semester = months/6
                volume = semester if months % 6 == 0 else semester + 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #standard V.A.1, V.A.2 for duties each year
        duty_year = ['V.A.1','V.A.2']
        duties_year = duties.filtered(lambda x: x.standard_id.code in duty_year) 

        if duties_year:
            for item in duties_year:
                standard = item.standard_id
                code = standard.code
                start = datetime.strptime(item.duty_id.start, '%Y-%m-%d')
                finish = datetime.strptime(item.duty_id.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.duty
                note = item.reference
                reference = 'itb.hr_duty,' + str(item.duty_id.id)
                today = datetime.today()
                
                if finish > today:
                    months = (today.year - start.year)*12 + today.month - start.month
                else:
                    months = (finish.year - start.year)*12 + finish.month - start.month
                
                year = months/12
                volume = year if months % 12 == 0 else year + 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #duty with max allowed
        duty_max = ['II.L.1','II.L.2']
        
        #standard II.L.1
        duties_IIl1 = duties.filtered(lambda x: x.standard_id.code == 'II.L.1')
        if duties_IIl1:
            last_semester = ''
            i = 1
            for item in duties_IIl1:
                standard = item.standard_id
                code = standard.code
                semester = semesters.filtered(lambda x: x.start <= item.duty_id.start and x.finish >= item.duty_id.start)
                period = semester.name
                name = item.duty
                note = item.reference
                reference = 'itb.hr_duty,' + str(item.duty_id.id)
                if i == 1:
                    last_semester = period
                else:
                    if period != last_semester:
                        i = 1                            
                    
                if i<=1:
                    score_max = standard.score
                else:
                    score_max = 0

                volume = 1
                score = volume * score_max
                last_semester = period
                i = i + 1
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                result.append(output)


        #standard II.L.2
        duties_IIl2 = duties.filtered(lambda x: x.standard_id.code == 'II.L.2')
        if duties_IIl2:
            last_semester = ''
            i = 1
            for item in duties_IIl2:
                standard = item.standard_id
                code = standard.code
                semester = semesters.filtered(lambda x: x.start <= item.duty_id.start and x.finish >= item.duty_id.start)
                period = semester.name
                name = item.duty
                note = item.reference
                reference = 'itb.hr_duty,' + str(item.duty_id.id)
                if i == 1:
                    last_semester = period
                else:
                    if period != last_semester:
                        i = 1                            
                    
                if i<=1:
                    score_max = standard.score
                else:
                    score_max = 0

                volume = 1
                score = volume * score_max
                last_semester = period
                i = i + 1
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                result.append(output)


        #standard for all other duties
        duty_exclude = duty_semester + duty_year + duty_max
        duties_other = duties.filtered(lambda x: x.standard_id.code not in duty_exclude) 

        if duties_other:
            for item in duties_other:
                standard = item.standard_id
                code = standard.code
                start = datetime.strptime(item.duty_id.start, '%Y-%m-%d')
                finish = datetime.strptime(item.duty_id.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.duty
                note = item.reference
                reference = 'itb.hr_duty,' + str(item.duty_id.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #standard II.D
        supervisors = self.env['itb.academic_supervisor'].search([('employee_id.id','=',self.employee_id.id),('thesis_id.graduation','>=',last_jabatan.start)],order='semester')

        if supervisors:
            #standard II.D.1.a
            supervisors_IId1a = supervisors.filtered(lambda x: x.role=='lead' and x.thesis_id.category=='disertasi')
            if supervisors_IId1a:
                last_semester = ''
                i = 1
                for item in supervisors_IId1a:
                    code = 'II.D.1.a' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=4:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.D.1.b
            supervisors_IId1b = supervisors.filtered(lambda x: x.role=='lead' and x.thesis_id.category=='thesis')
            if supervisors_IId1b:
                last_semester = ''
                i = 1
                for item in supervisors_IId1b:
                    code = 'II.D.1.b' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=6:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.D.1.c
            supervisors_IId1c = supervisors.filtered(lambda x: x.role=='lead' and x.thesis_id.category=='skripsi')
            
            if supervisors_IId1c:
                last_semester = ''
                i = 1
                for item in supervisors_IId1c:
                    code = 'II.D.1.c' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    if i<=8:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)

            #standard II.D.2.a
            supervisors_IId2a = supervisors.filtered(lambda x: x.role=='assistant' and x.thesis_id.category=='disertasi')
            if supervisors_IId2a:
                last_semester = ''
                i = 1
                for item in supervisors_IId2a:
                    code = 'II.D.2.a' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=4:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.D.2.b
            supervisors_IId2b = supervisors.filtered(lambda x: x.role=='assistant' and x.thesis_id.category=='thesis')
            if supervisors_IId2b:
                last_semester = ''
                i = 1
                for item in supervisors_IId2b:
                    code = 'II.D.2.b' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=6:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.D.2.c
            supervisors_IId2c = supervisors.filtered(lambda x: x.role=='assistant' and x.thesis_id.category=='skripsi')
            if supervisors_IId2c:
                last_semester = ''
                i = 1
                for item in supervisors_IId2c:
                    code = 'II.D.2.c' 
                    standard = standards.filtered(lambda r: r.code == code)
                    period = item.semester
                    name = item.thesis_id.authors
                    note = ''
                    reference = 'itb.academic_thesis,' + str(item.thesis_id.id)                    
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=8:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


        #standard II.E
        testers = self.env['itb.academic_tester'].search([('employee_id.id','=',self.employee_id.id),('defence_id.thesis_id.graduation','>=',last_jabatan.start)])

        if testers:
            for item in testers:
                if item.role == 'lead':
                    code = 'II.E.1'
                if item.role == 'assistant':
                    code = 'II.E.2'
                
                standard = standards.filtered(lambda r: r.code == code)
                period = item.defence_id.thesis_id.graduation_semester.name
                name = item.defence_id.thesis_id.authors
                note = ''
                reference = 'itb.academic_tester,' + str(item.defence_id.thesis_id.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)


        #standard II.F
        counselors = self.env['itb.academic_counselor'].search([('employee_id.id','=',self.employee_id.id),('semester_id.finish','>=',last_jabatan.start)])

        if counselors:
            sems = counselors.mapped('semester_id.name')
            code = 'II.F'                
            standard = standards.filtered(lambda r: r.code == code)

            for semester in sems:
                 #students = [x.partner_id.name + ' (' + x.partner_id.student_id + ')' for x in counselors if x.semester_id.name==semester]
                students1 = ['20' + x.partner_id.student_id[3:5] for x in counselors if x.semester_id.name==semester]
                students = sorted(set(students1))
                period = semester
                #name = ', '.join(students)
                name = 'Membina kegiatan mahasiswa angkatan ' + ', '.join(students)
                note = ''
                reference = 'hr.employee,' + str(self.employee_id.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)

        
        # all publication related standard in Lamp2, Lamp3, Lamp4, Lamp5.special treatment for standard II.H and II.I, and III        
        if publications:
            pub_HI = ['II.H.1','II.H.2','II.I']
            #standard II.H.1 
            publications_IIh1 = publications.filtered(lambda x: x.publication_id.standard_id.code == 'II.H.1')
            if publications_IIh1:
                last_year = ''
                i = 1
                for item in publications_IIh1:
                    standard = item.publication_id.standard_id
                    code = standard.code
                    period = datetime.strptime(item.day, '%Y-%m-%d').strftime('%Y')
                    scopus = item.publication_id.scopus if item.publication_id.scopus else ''
                    name = item.publication_id.authors + ', "' + item.publication_id.name + '", ' + item.publication_id.publisher + ', ' + datetime.strptime(item.publication_id.day, '%Y-%m-%d').strftime('%d %B %Y') + ', ' + scopus
                    note = ''
                    reference = 'itb.hr_publication,' + str(item.publication_id.id)
                    if i == 1:
                        last_year = period
                    else:
                        if period != last_year:
                            i = 1                            
                    
                    if i<=1:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_year = period
                    i = i + 1      
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.H.2
            publications_IIh2 = publications.filtered(lambda x: x.publication_id.standard_id.code == 'II.H.2')
            if publications_IIh2:
                last_semester = ''
                i = 1
                for item in publications_IIh2:
                    standard = item.publication_id.standard_id
                    code = standard.code
                    semester = semesters.filtered(lambda x: x.start <= item.publication_id.day and x.finish >= item.publication_id.day)
                    period = semester.name
                    scopus = item.publication_id.scopus if item.publication_id.scopus else ''
                    name = item.publication_id.authors + ', "' + item.publication_id.name + '", ' + item.publication_id.publisher + ', ' + datetime.strptime(item.publication_id.day, '%Y-%m-%d').strftime('%d %B %Y') + ', ' + scopus
                    note = ''
                    reference = 'itb.hr_publication,' + str(item.publication_id.id)
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=1:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)


            #standard II.I
            publications_IIi = publications.filtered(lambda x: x.publication_id.standard_id.code == 'II.I')
            if publications_IIi:
                last_semester = ''
                i = 1
                for item in publications_IIi:
                    standard = item.publication_id.standard_id
                    code = standard.code
                    semester = semesters.filtered(lambda x: x.start <= item.publication_id.day and x.finish >= item.publication_id.day)
                    period = semester.name
                    scopus = item.publication_id.scopus if item.publication_id.scopus else ''
                    name = item.publication_id.authors + ', "' + item.publication_id.name + '", ' + item.publication_id.publisher + ', ' + datetime.strptime(item.publication_id.day, '%Y-%m-%d').strftime('%d %B %Y') + ', ' + scopus
                    note = ''
                    reference = 'itb.hr_publication,' + str(item.publication_id.id)
                    if i == 1:
                        last_semester = period
                    else:
                        if period != last_semester:
                            i = 1                            
                    
                    if i<=2:
                        score_max = standard.score
                    else:
                        score_max = 0

                    volume = 1
                    score = volume * score_max
                    last_semester = period
                    i = i + 1
                    output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':score_max,'reference':reference,'note':note})
                    result.append(output)
            
            
            #special shared scoring for standard III
            pub_III = ['III.A.1.a.1','III.A.1.a.2','III.A.1.b.1','III.A.1.b.2','III.A.1.b.3','III.A.1.c.1.a','III.A.1.c.1.b','III.B','III.C','III.D.1','III.D.2','III.E.1','III.E.2','III.E.3']
            publications_shared = publications.filtered(lambda x: x.publication_id.standard_id.code in pub_III)
            for item in publications_shared:
                standard = item.publication_id.standard_id
                code = standard.code
                semester = semesters.filtered(lambda x: x.start <= item.publication_id.day and x.finish >= item.publication_id.day)
                period = semester.name
                scopus = item.publication_id.scopus if item.publication_id.scopus else ''
                authors = item.publication_id.authors if item.publication_id.authors else ''
                title = item.publication_id.name if item.publication_id.name else ''
                publisher = item.publication_id.publisher if item.publication_id.publisher else ''
                day = datetime.strptime(item.publication_id.day, '%Y-%m-%d').strftime('%d %B %Y') if item.publication_id.day else ''
                name = authors + ', "' + title + '", ' + publisher + ', ' + day + ', ' + scopus
                note = ''
                reference = 'itb.hr_publication,' + str(item.publication_id.id)
                volume = 1
                
                if item.publication_id.state in ['draft','confirm']:
                    if item.role == 'author':
                        score = 0.6 * standard.score
                    if item.role == 'co-author':
                        score = 0.4 * standard.score / (item.publication_id.authors_count * 1.0)
                if item.publication_id.state in ['review','validate']:
                    score = item.score

                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)

           
            #all other publication related standards
            pub_exclude = pub_HI + pub_III
            publications_other = publications.filtered(lambda x: x.publication_id.standard_id.code not in pub_exclude)
            for item in publications_other:
                standard = item.publication_id.standard_id
                code = standard.code
                semester = semesters.filtered(lambda x: x.start <= item.publication_id.day and x.finish >= item.publication_id.day)
                period = semester.name
                scopus = item.publication_id.scopus if item.publication_id.scopus else ''
                name = item.publication_id.authors + ', "' + item.publication_id.name + '", ' + item.publication_id.publisher + ', ' + datetime.strptime(item.publication_id.day, '%Y-%m-%d').strftime('%d %B %Y') + ', ' + scopus
                note = ''
                reference = 'itb.hr_publication,' + str(item.publication_id.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)



        #standard II.J
        assignments = self.env['itb.hr_assignment'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start),('standard_id','!=',False)])
        
        if assignments:
            for item in assignments:
                standard = item.standard_id
                code = standard.code
                start = datetime.strptime(item.start, '%Y-%m-%d')
                finish = datetime.strptime(item.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.job_id.name
                note = item.reference
                reference = 'itb.hr_assignment,' + str(item.id)
                today = datetime.today()
                
                if finish > today:
                    months = (today.year - start.year)*12 + today.month - start.month
                else:
                    months = (finish.year - start.year)*12 + finish.month - start.month
                
                semester = months/6
                volume = semester if months % 6 == 0 else semester + 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)



        #standard II.M
        trainings = self.env['itb.hr_training'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start),('standard_id','!=',False),('standard_id.code','!=','I.A.B.2')])
        
        if trainings:
            for item in trainings:
                standard = item.standard_id
                code = standard.code
                period = datetime.strptime(item.start, '%Y-%m-%d').strftime('%d %B %Y') + ' - ' +  datetime.strptime(item.finish, '%Y-%m-%d').strftime('%d %B %Y')
                name = item.name
                note = ''
                reference = 'itb.hr_training,' + str(item.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)

        

        #standard IV.A
        works = self.env['itb.hr_work'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start)])
        
        if works:
            for item in works:
                code = 'IV.A'
                standard = standards.filtered(lambda r: r.code == code)
                start = datetime.strptime(item.start, '%Y-%m-%d')
                finish = datetime.strptime(item.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.name
                note = item.reference
                reference = 'itb.hr_work,' + str(item.id)
                today = datetime.today()
                
                if finish > today:
                    months = (today.year - start.year)*12 + today.month - start.month
                else:
                    months = (finish.year - start.year)*12 + finish.month - start.month
                
                semester = months/6
                volume = semester if months % 6 == 0 else semester + 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)



        #standard IV.D
        projects = self.env['itb.hr_project_team'].search([('employee_id.id','=',self.employee_id.id),('project_id.start','>=',last_jabatan.start),('project_id.standard_id','!=',False)])
        
        if projects:
            for item in projects:
                standard = item.project_id.standard_id
                code = standard.code
                start = datetime.strptime(item.project_id.start, '%Y-%m-%d')
                finish = datetime.strptime(item.project_id.finish, '%Y-%m-%d')
                period = start.strftime('%d %B %Y') + ' - ' +  finish.strftime('%d %B %Y')
                name = item.project_id.name
                note = item.project_id.reference
                reference = 'itb.hr_project,' + str(item.project_id.id)
                today = datetime.today()
                
                if finish > today:
                    months = (today.year - start.year)*12 + today.month - start.month
                else:
                    months = (finish.year - start.year)*12 + finish.month - start.month
                
                semester = months/6
                volume = semester if months % 6 == 0 else semester + 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)




        #standard V.C
        memberships = self.env['itb.hr_membership'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start)])
        
        if memberships:
            for item in memberships:
                if item.level == 'global' and item.role == 'leader':
                    code = 'V.C.1.a'
                if item.level == 'global' and item.role == 'honor':
                    code = 'V.C.1.b'
                if item.level == 'global' and item.role == 'member':
                    code = 'V.C.1.c'
                if item.level == 'national' and item.role == 'leader':
                    code = 'V.C.2.a'
                if item.level == 'national' and item.role == 'honor':
                    code = 'V.C.2.b'
                if item.level == 'national' and item.role == 'member':
                    code = 'V.C.2.c'
                
                standard = standards.filtered(lambda r: r.code == code)
                period = datetime.strptime(item.start, '%Y-%m-%d').strftime('%d %B %Y') + ' - ' +  datetime.strptime(item.finish, '%Y-%m-%d').strftime('%d %B %Y')
                name = item.name
                note = ''
                reference = 'itb.hr_membership,' + str(item.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)



        #standard V.G, V.I
        awards = self.env['itb.hr_award'].search([('employee_id.id','=',self.employee_id.id),('start','>=',last_jabatan.start),('standard_id','!=',False)])
        
        if awards:
            for item in awards:
                standard = item.standard_id
                code = standard.code
                period = datetime.strptime(item.start, '%Y-%m-%d').strftime('%d %B %Y')
                name = item.name
                note = item.reference
                reference = 'itb.hr_award,' + str(item.id)
                volume = 1
                score = volume * standard.score
                output = (0,0,{'name':name,'standard_id':standard.id,'code':code,'unit':standard.unit,'period':period,'volume':volume,'score':score,'score_max':standard.score,'reference':reference,'note':note})
                result.append(output)



        #remove existing dupak line and add updated ones
        self.write({'line_ids': [(2,line.id) for line in self.line_ids]})  
        self.write({'finish':fields.Date.today(),'line_ids':result})


        #res1=result

class Dupak_Line(models.Model):
    _name = 'itb.dupak_line'
    _order = 'code,period'
    
    name = fields.Char(index=True)
    dupak_id = fields.Many2one('itb.dupak',string="DUPAK",required=True,index=True)
    standard_id = fields.Many2one('itb.dupak_standard',string="Standard",required=True,index=True)
    code = fields.Char(related='standard_id.code', index=True,string="Code",store=True)
    unit = fields.Char(related='standard_id.unit',store=True)
    period = fields.Char()
    start = fields.Date()
    finish = fields.Date()
    volume = fields.Float()
    score_max = fields.Float()
    score = fields.Float()
    note = fields.Char()
    #reference = fields.Char()#fields.Reference([
    #reference = fields.Reference([
    #    ('itb.hr_assignment', 'Assignment'), 
    #    ('itb.hr_award', 'Award'),
    #    ('itb.hr_education', 'Education'),
    #    ('itb.hr_membership', 'Membership'),
    #    ('itb.hr_project_team', 'Project'),
    #    ('itb.hr_publication_author', 'Publication'),
    #    ('itb.hr_training', 'Training'),
    #    ('itb.hr_work', 'Work'),
    #    ('itb.academic_instructor', 'Teaching'),
    #    ('itb.academic_supervisor', 'Supervisor'),
    #    ('itb.academic_tester', 'Defender'),
    #    ('itb.academic_counselor', 'Counselor'),
    #    ],
    #'Refers to')
    reference = fields.Reference(selection='get_reference', string='Reference')

    @api.model
    def get_reference(self):
        records = self.env['ir.model'].search([('model','in',
            ['itb.hr_assignment',
            'itb.hr_award',
            'itb.hr_education',
            'itb.hr_membership',
            'itb.hr_project_team',
            'itb.hr_publication_author',
            'itb.hr_training',
            'itb.hr_work',
            'itb.academic_instructor',
            'itb.academic_supervisor',
            'itb.academic_tester',
            'itb.academic_counselor',
            'itb.academic_thesis'])])
        return [(record.model,record.name) for record in records] + [('','')]

class DupakExcel(ReportXlsx):
    def format_data(self,dupak):
        result = {}
        result2 = {}
        
        for line in dupak.line_ids:
            if line.code in result:
                if line.period in result[line.code]:
                    result[line.code][line.period].append(line)
                else:
                    result[line.code][line.period] = [line]
            else:
                result[line.code] ={line.period:[line]}
        return result

    def generate_xlsx_report(self, workbook, data, dupak):
        #format data
        result = self.format_data(dupak)
        res1= result

        #hold summary address cell for each code
        total = {}

        #generate all worksheer
        sheet1 = workbook.add_worksheet('Lamp.1')
        sheet2 = workbook.add_worksheet('Lamp.2')
        sheet3 = workbook.add_worksheet('Lamp.3')
        sheet4 = workbook.add_worksheet('Lamp.4')
        sheet5 = workbook.add_worksheet('Lamp.5')
        sheet6 = workbook.add_worksheet('Lamp.6')

        #configurable default value
        conf_school = 'Sekolah Teknik Elektro dan Informatika ITB'
        conf_wds_name = 'Dr.Ir. Nana Rachmana Syambas, M.Eng.'
        conf_wds_nip = '19660228 199102 1 001'
        conf_wds_pangkat = 'Pembina Tk. I, Gol. IVb, 1 April 2002'
        conf_wrso_name = 'Prof.Dr. Irawati, MS'
        conf_wrso_nip = '195904181983032001'

        #generic format
        fmt_headerwrap = workbook.add_format({'bold':True,'text_wrap':True})
        fmt_headercenter = workbook.add_format({'bold':True,'align':'center'})
        fmt_columnheader = workbook.add_format({'bold':True,'valign':'top','align':'center','text_wrap':True,'border':True})
        fmt_centerbox = workbook.add_format({'align':'center','border':True})
        fmt_center = workbook.add_format({'align':'center'})
        fmt_wrap = workbook.add_format({'text_wrap':True,'valign':'top'})
        fmt_default = workbook.add_format({'valign':'top','text_wrap':True})
        fmt_box = workbook.add_format({'border':True,'valign':'top','text_wrap':True})
        
        #sheet Lamp 2
        sheet2.set_column('A:A',3)
        sheet2.set_column('B:F',2.75)
        sheet2.set_column('G:I',4.30)
        sheet2.set_column('J:J',11.7)
        sheet2.set_column('K:K',9.43)
        sheet2.set_column('L:L',7)
        sheet2.set_column('M:M',5)
        sheet2.set_column('N:N',7.5)
        sheet2.set_row(0,6.75)
        sheet2.write('K2','Lampiran II:', fmt_wrap)
        sheet2.set_row(1,122.25)
        sheet2.merge_range('L2:O2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet2.merge_range('A6:O6','SURAT PERNYATAAN',fmt_headercenter)
        sheet2.merge_range('A7:O7','MELAKSANAKAN PENDIDIKAN',fmt_headercenter)
        sheet2.write('A9','Yang bertanda tangan di bawah ini:')
        sheet2.set_row(9,6)
        sheet2.write('C11','Nama')
        sheet2.write('C12','NIP')
        sheet2.write('C13','Pangkat/Golongan Ruang/TMT')
        sheet2.write('C14','Jabatan')
        sheet2.write('C15','Unit Kerja')
        sheet2.write('J11',': ' + conf_wds_name)
        sheet2.write('J12',': ' + conf_wds_nip)
        sheet2.write('J13',': ' + conf_wds_pangkat)
        sheet2.write('J14',': Wakil Dekan Bidang Sumberdaya')
        sheet2.write('J15',': ' + conf_school)
        sheet2.set_row(15,6)
        sheet2.write('A17','Menyatakan bahwa:')
        sheet2.set_row(17,6)
        sheet2.write('C19','Nama')
        sheet2.write('C20','NIP')
        sheet2.write('C21','Pangkat/Golongan Ruang/TMT')
        sheet2.write('C22','Jabatan')
        sheet2.write('C23','Unit Kerja')
        sheet2.write('J19',': ' + dupak.employee_id.name)
        sheet2.write('J20',': ' + dupak.employee_id.nip_new)
        sheet2.write('J21',': ' + dupak.pangkat)
        #import pdb;pdb.set_trace()
        sheet2.write('J22',': ' + dupak.jabatan)
        sheet2.write('J23',': ' + conf_school)
        sheet2.write('A25','Telah melaksanakan pendidikan sebagai berikut:')
        sheet2.write('A27','No.',fmt_columnheader)
        sheet2.merge_range('B27:I27','Uraian Kegiatan',fmt_columnheader)
        sheet2.write('J27','Tanggal',fmt_columnheader)
        sheet2.write('K27','Satuan Hasil',fmt_columnheader)
        sheet2.write('L27','Jumlah Volume Kegiatan',fmt_columnheader)
        sheet2.write('M27','Angka Kredit',fmt_columnheader)
        sheet2.write('N27','Jumlah Angka Kredit',fmt_columnheader)
        sheet2.write('O27','Keterangan/Bukti Fisik',fmt_columnheader)
        sheet2.write('A28','1.',fmt_centerbox)
        sheet2.merge_range('B28:I28','2.',fmt_centerbox)
        sheet2.write('J28','3.',fmt_centerbox)
        sheet2.write('K28','4.',fmt_centerbox)
        sheet2.write('L28','5.',fmt_centerbox)
        sheet2.write('M28','6.',fmt_centerbox)
        sheet2.write('N28','7.',fmt_centerbox)
        sheet2.write('O28','8.',fmt_centerbox)
        current_row2 = 29
#===========================BEGIN REVISI TGL 03 AGUSTUS 2017 BY IDRIS=======================================
        def getSort(self):
            dic = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', 'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6'}
            if '/' in self:
                getSort = self[len(self)-9:len(self)-5] + '-' + dic[self[0:len(self)-10]]
            else:
                dt = []
                dt = self.split(' - ')
                if dt :
                    #datetime.strptime(text, '%Y-%m-%d')
                    getSort = datetime.strptime(dt[0], '%d %B %Y') #dt[0]#self[len(self)-9:len(self)-5] + '-' + dic[self[0:len(self)-10]]
            return getSort

        def getSmt(self):
            dc = {'1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V', '6': 'VI', 'I': 'I', 'II': 'II', 'III': 'III', 'IV': 'IV', 'V': 'V', 'VI': 'VI'}
            if '/' in self:
                getSmt = 'sem ' + dc[self[0:len(self)-10]] + ' ' + self[len(self)-7:len(self)-5] + '/' + self[len(self)-2:len(self)]
            return getSmt

#===========================END REVISI TGL 03 AGUSTUS 2017 BY IDRIS=======================================        
        if any(k in result for k in ['I.A.1','I.A.2','I.B']):
            sheet2.write('A' + str(current_row2),'I')
            sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'PENDIDIKAN',fmt_box)
            for x in ['J','K','L','M','N','O']:
                sheet2.write(x + str(current_row2),'',fmt_box)
            current_row2 = current_row2 + 1

            if any(k in result for k in ['I.A.1','I.A.2']):
                sheet2.write('A' + str(current_row2),'I.A')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Pendidikan Formal',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1

                if 'I.A.1' in result and any(result['I.A.1']):
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'1. Doktor (S3)',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    for period,lines in result['I.A.1'].items():
                        if len(lines) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),period,fmt_box)

                        for line in lines:
                            sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            current_row2 = current_row2 + 1
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                    
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total I.A.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['I.A.1'] = '=Lamp.2!N' + str(current_row2)
                    current_row2 = current_row2 + 1


                if 'I.A.2' in result and any(result['I.A.2']):
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'2. Magister (S2)',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                    
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    for period,lines in result['I.A.2'].items():
                        if len(lines) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),period,fmt_box)

                        for line in lines:
                            sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            current_row2 = current_row2 + 1
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total I.A.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['I.A.2'] = '=Lamp.2!N' + str(current_row2)
                    current_row2 = current_row2 + 1


            if any(k in result for k in ['I.B']):
                sheet2.write('A' + str(current_row2),'I.B')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Diklat Pra Jabatan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2

                if 'I.B' in result and any(result['I.B']):
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Diklat Prajabatan golongan III',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                   
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    for period,lines in result['I.A.B.2'].items():
                        if len(lines) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),period,fmt_box)

                        for line in lines:
                            sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            current_row2 = current_row2 + 1
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total I.B',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['I.B'] = '=Lamp.2!N' + str(current_row2)
                    current_row2 = current_row2 + 1


        if any(k in result for k in ['II.A','II.B','II.C','II.D.1.a','II.D.1.b','II.D.1.c','II.D.2.a','II.D.2.b','II.D.2.c','II.E.1','II.E.2','II.F','II.G','II.H.1','II.H.2','II.I','II.J.1','II.J.2','II.J.3','II.J.4','II.J.5','II.J.6','II.J.7.','II.J.8','II.K.1','II.K.2','II.L.1','II.L.2','II.M.1','II.M.2','II.M.3','II.M.4','II.M.5','II.M.6','II.M.7']):
            sheet2.write('A' + str(current_row2),'II')
            sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'PELAKSANAAN PENDIDIKAN',fmt_box) 
            for x in ['J','K','L','M','N','O']:
                 sheet2.write(x + str(current_row2),'',fmt_box)
            current_row2 = current_row2 + 1

            if 'II.A' in result and any(result['II.A']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.A'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                no = 1
                sheet2.write('A' + str(current_row2),'II.A')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Melaksanakan perkuliahan/tutorial dan membimbing, menguji serta menyelenggarakan pendidikan di lab., praktik keguruan, bengkel/studio/kebun percobaan/ teknologi pengajaran dan praktik lapangan',fmt_box)
                sheet2.set_row(current_row2-1,106.5)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2 
                
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.A']:
                        dat = result['II.A'][sem]
                #=============================================================
                    #for period,lines in result['II.A'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat)),getSmt(sem),fmt_box)
                        else:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + 1),getSmt(sem),fmt_box)
                            #sheet2.write('J' + str(current_row2),sem,fmt_box)
                        tsks = sum([x.volume for x in dat])
                        mline = len([x.volume for x in dat])

                        i = 1
                        sc = 0
                        sct = 0
                        for line in dat:
                        #for line in lines:
                            sheet2.set_row(current_row2-1,30)
                            sheet2.write('B' + str(current_row2),no,fmt_box)
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('K' + str(current_row2),'',fmt_box)
                            #sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            #sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            #sheet2.write('N' + str(current_row2),line.score,fmt_box)
                            if i == 1:
                                if tsks > 10:
                                    sheet2.write('L' + str(current_row2),10,fmt_box)
                                    if not(dupak.jabatan) == 'Asisten Ahli':
                                        sheet2.write('M' + str(current_row2),'1',fmt_box)
                                        sheet2.write('N' + str(current_row2),10,fmt_box)
                                        sc=10
                                    else:
                                        sheet2.write('M' + str(current_row2),'0.5',fmt_box)
                                        sheet2.write('N' + str(current_row2),5,fmt_box)
                                        sc = 5
                                else:
                                    sheet2.write('L' + str(current_row2),tsks,fmt_box)
                                    if not(dupak.jabatan) == 'Asisten Ahli':
                                        sheet2.write('M' + str(current_row2),'1',fmt_box)
                                        sheet2.write('N' + str(current_row2),tsks,fmt_box)
                                        sc = tsks
                                    else:
                                        sheet2.write('M' + str(current_row2),'0.5',fmt_box)
                                        sheet2.write('N' + str(current_row2),tsks/2,fmt_box)
                                        sc = tsks/2
                            elif i == 2 and tsks > 10:
                                sheet2.write('L' + str(current_row2),tsks-10,fmt_box)
                                if not(dupak.jabatan) == 'Asisten Ahli':
                                    sheet2.write('M' + str(current_row2),'0.5',fmt_box)
                                    sheet2.write('N' + str(current_row2),(tsks-10)/2,fmt_box)
                                    sc = (tsks-10)/2
                                else:
                                    sheet2.write('M' + str(current_row2),'0.25',fmt_box)
                                    sheet2.write('N' + str(current_row2),(tsks-10)/4,fmt_box)
                                    sc = (tsks-10)/4
                            else:
                                sheet2.write('L' + str(current_row2),'',fmt_box)
                                sheet2.write('M' + str(current_row2),'',fmt_box)
                                sheet2.write('N' + str(current_row2),'',fmt_box)
                                sc = 0
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            
                            sct = sct + sc
                            if i == mline:
                                current_row2 = current_row2 + 1
                                for x in ['B','J','K','L','M','N','O']:
                                    sheet2.write(x + str(current_row2),'',fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total - ' + sem + ' - ' + str(sct) + ' sks' ,fmt_box)
                            i += 1
                            no += 1
                            current_row2 = current_row2 + 1
                
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.A',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.A'] = '=Lamp.2!N' + str(current_row2)
                no += 1
                current_row2 = current_row2 + 1
                
            if 'II.B' in result and any(result['II.B']):
                 #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.B'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                no = 1
                sheet2.write('A' + str(current_row2),'II.B')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Membimbing seminar mahasiswa',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2

                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.B']:
                        dat = result['II.B'][sem]
                #=============================================================
                    #for period,lines in result['II.B'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                        
                        i =1
                        for line in dat:
                            sheet2.set_row(current_row2-1,30)
                            sheet2.write('B' + str(current_row2),no,fmt_box)
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            no += 1
                            i += 1
                            current_row2 = current_row2 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.B',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.B'] = '=Lamp.2!N' + str(current_row2)
                no += 1
                current_row2 = current_row2 + 1
                
            if 'II.C' in result and any(result['II.C']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.C'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                no = 1
                sheet2.write('A' + str(current_row2),'II.C')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Membimbing Kuliah Kerja Nyata, Praktik Kerja Nyata, Praktik Kerja Lapangan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2

                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.C']:
                        dat = result['II.C'][sem]
                #=============================================================
                    #for period,lines in result['II.C'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                        
                        i =1
                        for line in dat:
                            sheet2.set_row(current_row2-1,30)
                            sheet2.write('B' + str(current_row2),no,fmt_box)
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            no += 1
                            i += 1
                            current_row2 = current_row2 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.C',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.C'] = '=Lamp.2!N' + str(current_row2)
                no += 1
                current_row2 = current_row2 + 1
                

            if any(k in result for k in ['II.D.1.a','II.D.1.b','II.D.1.c','II.D.2.a','II.D.2.b','II.D.2.c']):
                sheet2.set_row(current_row2-1,45)
                sheet2.write('A' + str(current_row2),'II.D')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Membimbing & ikut membimbing dalam menghasilkan disertasi, thesis, skripsi & laporan akhir studi',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)                
                current_row2 = current_row2 + 1

#===========================BEGIN REVISI TGL 03 AGUSTUS 2017 BY IDRIS=======================================
                dumm = []
                code = ['II.D.1.a','II.D.1.b','II.D.1.c','II.D.2.a','II.D.2.b','II.D.2.c']
                for cod in code:
                    if cod in result and any(result[cod]):
                        for key,value in result[cod].items():
                            dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                
                #for x in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N']:
                #    sheet2.write(x + str(current_row2),'',fmt_box)
                #sheet2.write('O' + str(current_row2),len(semester),fmt_box)                
                #current_row2 = current_row2 + 1

                no = 1
                if any(k in result for k in ['II.D.1.a','II.D.1.b','II.D.1.c']):
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Pembimbing Utama',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                   
                    current_row2 = current_row2 + 1
                    start_code = current_row2
                    code = ['II.D.1.a','II.D.1.b','II.D.1.c']
                    for sem in semester:
                        for cod in code:
                            if cod in result and any(result[cod]):
                                if sem in result[cod]:
                                    dat = result[cod][sem]
                                    i = 1
                                    if len(dat) > 1:
                                        sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)

                                    for rec in dat:
                                        sheet2.set_row(current_row2-1,30)                        
                                        sheet2.write('C' + str(current_row2),no,fmt_box)
                                        sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),rec.name,fmt_box)
                                        sheet2.write('K' + str(current_row2),'',fmt_box)
                                        sheet2.write('L' + str(current_row2),rec.volume,fmt_box)
                                        sheet2.write('M' + str(current_row2),rec.score_max,fmt_box)
                                        sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                        sheet2.write('O' + str(current_row2),rec.note,fmt_box)
                                        no += 1
                                        i += 1
                                        current_row2 = current_row2 + 1
                                    

                if any(k in result for k in ['II.D.2.a','II.D.2.b','II.D.2.c']):
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Pembimbing Pendamping/Pembantu',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                   
                    current_row2 = current_row2 + 1
                    code = ['II.D.2.a','II.D.2.b','II.D.2.c']
                    for sem in semester:
                        for cod in code:
                            if cod in result and any(result[cod]):
                                if sem in result[cod]:
                                    dat = result[cod][sem]
                                    i = 1
                                    if len(dat) > 1:
                                        sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)

                                    for rec in dat:
                                        sheet2.set_row(current_row2-1,30)                        
                                        sheet2.write('C' + str(current_row2),no,fmt_box)
                                        sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),rec.name,fmt_box)
                                        sheet2.write('K' + str(current_row2),'',fmt_box)
                                        sheet2.write('L' + str(current_row2),rec.volume,fmt_box)
                                        sheet2.write('M' + str(current_row2),rec.score_max,fmt_box)
                                        sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                        sheet2.write('O' + str(current_row2),rec.note,fmt_box)
                                        no += 1
                                        i += 1
                                        current_row2 = current_row2 + 1                                    
                
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.2',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                #total['II.D.2'] = '=Lamp.2!N' + str(current_row2)
                current_row2 = current_row2 + 1
#===========================END REVISI TGL 03 AGUSTUS 2017 BY IDRIS=======================================

            #    if 'II.D.1.a' in result and any(result['II.D.1.a']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'a. Disertasi ',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.1.a'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30)                        
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1
  
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)                    
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.1.a',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.1.a'] = '=Lamp.2!N' + str(current_row2)
            #        no += 1
            #        current_row2 = current_row2 + 1

            #    if 'II.D.1.b' in result and any(result['II.D.1.b']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'b. Thesis',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.1.b'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30)
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.1.b',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.1.b'] = '=Lamp.2!N' + str(current_row2)
            #        no += 1
            #        current_row2 = current_row2 + 1
                
            #    if 'II.D.1.c' in result and any(result['II.D.1.c']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'c. Skripsi', fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)                    
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.1.c'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30,fmt_default)
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.1.c',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.1.c'] = '=Lamp.2!N' + str(current_row2)   
            #        no += 1             
            #        current_row2 = current_row2 + 1
                
            #    if any(k in result for k in ['II.D.2.a','II.D.2.b','II.D.2.c']):
            #        sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Pembimbing Pendamping/Pembantu',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        current_row2 = current_row2 + 1

            #    if 'II.D.2.a' in result and any(result['II.D.2.a']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'a. Disertasi',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)                    
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.2.a'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30,fmt_default)
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1

            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.2.a',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.2.a'] = '=Lamp.2!N' + str(current_row2)
            #        no += 1
            #        current_row2 = current_row2 + 1
                
            #    if 'II.D.2.b' in result and any(result['II.D.2.b']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'b. Thesis',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.2.b'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30,fmt_default)
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.2.b',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.2.b'] = '=Lamp.2!N' + str(current_row2)
            #        no += 1
            #        current_row2 = current_row2 + 1
                
            #    if 'II.D.2.c' in result and any(result['II.D.2.c']):
            #        no = 1
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'c. Skripsi',fmt_box)
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        current_row2 = current_row2 + 1
            #        start_code = current_row2

            #        for period,lines in sorted(result['II.D.2.c'].items()):
            #            if len(lines) > 1:
            #                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(lines) - 1),period,fmt_box)
            #            else:
            #                sheet2.write('J' + str(current_row2),period,fmt_box)
                        
            #            i = 1
            #            for line in lines:
            #                sheet2.set_row(current_row2-1,30,fmt_default)
            #                sheet2.write('C' + str(current_row2),no,fmt_box)
            #                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
            #                sheet2.write('K' + str(current_row2),'',fmt_box)
            #                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
            #                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
            #                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
            #                sheet2.write('O' + str(current_row2),line.note,fmt_box)
            #                no += 1
            #                i += 1
            #                current_row2 = current_row2 + 1
            #        for x in ['J','K','L','M','N','O']:
            #            sheet2.write(x + str(current_row2),'',fmt_box)
            #        sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.D.2.c',fmt_box)
            #        sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
            #        total['II.D.2.c'] = '=Lamp.2!N' + str(current_row2)
            #        no += 1
            #        current_row2 = current_row2 + 1
            
            if any(k in result for k in ['II.E.1','II.E.2']):
                sheet2.write('A' + str(current_row2),'II.E')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Bertugas sebagai penguji pada ujian akhir',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2
                
                if 'II.E.1' in result and any(result['II.E.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.E.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'1. Ketua Penguji',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.E.1']:
                            dat = result['II.E.1'][sem]
                    #=============================================================

                        #for period,lines in result['II.E.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30,fmt_default)
                                sheet2.write('C' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('K' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.E.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.E.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1
                
                if 'II.E.2' in result and any(result['II.E.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.E.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'2. Anggota Penguji',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.E.2']:
                            dat = result['II.E.2'][sem]
                    #=============================================================
                    #for period,lines in result['II.E.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30,fmt_default)
                                sheet2.write('C' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('D' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('K' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.E.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.E.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1
                
            if 'II.F' in result and any(result['II.F']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.F'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                no =  1
                sheet2.set_row(current_row2-1,30,fmt_default)
                sheet2.write('A' + str(current_row2),'II.F')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Membina kegiatan mahasiswa di bidang Akademik dan kemahasiswaan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2

                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.F']:
                        dat = result['II.F'][sem]
                #=============================================================
                    #for period,lines in result['II.F'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                        for line in dat:
                            sheet2.set_row(current_row2-1,60,fmt_default)
                            sheet2.write('B' + str(current_row2),no,fmt_box)
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('K' + str(current_row2),'',fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            no += 1
                            current_row2 = current_row2 + 1
                            
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.F',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.F'] = '=Lamp.2!N' + str(current_row2)
                no += 1
                current_row2 = current_row2 + 1
            
            if 'II.G' in result and any(result['II.G']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.G'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet2.write('A' + str(current_row2),'II.G')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Mengembangkan program kuliah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)             
                current_row2 = current_row2 + 1
                start_code = current_row2
                
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.G']:
                        dat = result['II.G'][sem]
                #=============================================================
                    #for period,lines in result['II.G'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                        for line in dat:
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            current_row2 = current_row2 + 1
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),'Total II.G',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.G'] = '=Lamp.2!N' + str(current_row2)
                current_row2 = current_row2 + 1


            if any(k in result for k in ['II.H.1','II.H.2']):
                sheet2.write('A' + str(current_row2),'II.H')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Mengembangkan bahan kuliah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                
                if 'II.H.1' in result and any(result['II.H.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.H.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Buku Ajar',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.H.1']:
                            dat = result['II.H.1'][sem]
                    #=============================================================
                        #for period,lines in result['II.H.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.H.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.H.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.H.2' in result and any(result['II.H.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.H.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Diktat, modul, petunjuk praktikum, model, alat bantu, audio visual, naskah tutorial',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.H.2']:
                            dat = result['II.H.2'][sem]
                    #=============================================================
                        #for period,lines in result['II.H.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.H.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.H.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1



            if 'II.I' in result and any(result['II.I']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['II.I'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet2.write('A' + str(current_row2),'II.I')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Menyampaikan orasi ilmiah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                start_code = current_row2

                #=====================revisi==================================
                for sem in semester:
                    if sem in result['II.I']:
                        dat = result['II.I'][sem]
                #=============================================================
                    #for period,lines in result['II.I'].items():
                        if len(dat) > 1:
                            sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                        for line in dat:
                            sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                            sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                            sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                            sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                            sheet2.write('O' + str(current_row2),line.note,fmt_box)
                            current_row2 = current_row2 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.I',fmt_box)
                sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                total['II.I'] = '=Lamp.2!N' + str(current_row2)
                current_row2 = current_row2 + 1



            if any(k in result for k in ['II.J.1','II.J.2','II.J.3','II.J.4','II.J.5','II.J.6','II.J.7.','II.J.8']):
                sheet2.write('A' + str(current_row2),'II.J')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Menduduki jabatan pimpinan perguruan tinggi',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                
                if 'II.J.1' in result and any(result['II.J.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Rektor',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.1']:
                            dat = result['II.J.1'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.2' in result and any(result['II.J.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Pembantu Rektor/Dekan/Direktur PPs',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)        
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.2']:
                            dat = result['II.J.2'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30,fmt_box)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.3' in result and any(result['II.J.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'3. Ketua Sekolah Tinggi/Pembantu Dekan/ Asisten Dir. Program Pasca Sarjana/ Dir. Politeknik',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.3']:
                            dat = result['II.J.3'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.3'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.3',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.3'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.4' in result and any(result['II.J.4']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.4'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'4. Pembantu Ketua Sekolah Tinggi/Pembantu Direktur Politeknik',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)                    
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.4']:
                            dat = result['II.J.4'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.4'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.4',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.4'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.5' in result and any(result['II.J.5']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.5'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'5. Direktur Akademik',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.5']:
                            dat = result['II.J.5'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.5'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.5',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.5'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.6' in result and any(result['II.J.6']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.6'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'6. Pembantu Dir. Akademi/Ketua Jurusan/ Bagian pada Univ/Inst/Sekolah Tinggi',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.6']:
                            dat = result['II.J.6'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.6'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.6',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.6'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.7' in result and any(result['II.J.7']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.7'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'7. Ketua Jurusan pada Politeknik/Akademi/ Sekretaris Jurusan/Bagian pada Univ/Inst/ST.',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.7']:
                            dat = result['II.J.7'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.7'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.7',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.7'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.J.8' in result and any(result['II.J.8']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.J.8'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'8. Sekretaris Jurusan pada Politeknik/Akademi/ Sekretaris Jurusan/Bagian pada Univ/Inst/ST.',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)  
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.J.8']:
                            dat = result['II.J.8'][sem]
                    #=============================================================
                        #for period,lines in result['II.J.8'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.J.8',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.J.8'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


            if any(k in result for k in ['II.K.1','II.K.2']):
                sheet2.write('A' + str(current_row2),'II.K')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Membimbing Dosen yang lebih rendah jabatannya',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    heet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                
                if 'II.K.1' in result and any(result['II.K.1']):
                    no = 1
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.K.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Pembimbing pencakokan',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.K.1']:
                            dat = result['II.K.1'][sem]
                    #=============================================================
                        #for period,lines in result['II.K.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.K.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.K.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.K.2' in result and any(result['II.K.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.K.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Reguler',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.K.2']:
                            dat = result['II.K.2'][sem]
                    #=============================================================
                        #for period,lines in result['II.K.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.K.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.K.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


            if any(k in result for k in ['II.L.1','II.L.2']):
                sheet2.write('A' + str(current_row2),'II.L')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Melaksanakan kegiatan detasering & pencangkokan Akademik Dosen',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                
                if 'II.L.1' in result and any(result['II.L.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.L.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Detasering',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.L.1']:
                            dat = result['II.L.1'][sem]
                    #=============================================================
                        #for period,lines in result['II.L.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.L.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.L.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.L.2' in result and any(result['II.L.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.L.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Pencangkokan',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.L.2']:
                            dat = result['II.L.2'][sem]
                    #=============================================================
                        #for period,lines in result['II.L.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max, fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.L.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.L.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


            if any(k in result for k in ['II.M.1','II.M.2','II.M.3','II.M.4','II.M.5','II.M.6','II.M.7']):
                sheet2.write('A' + str(current_row2),'II.M')
                sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Melakukan kegiatan pengembangan diri untuk meningkatkan kompetensi',fmt_box)
                for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                current_row2 = current_row2 + 1
                
                if 'II.M.1' in result and any(result['II.M.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'1. Lamanya lebih dari 960 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.1']:
                            dat = result['II.M.1'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.1'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.1',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.1'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.2' in result and any(result['II.M.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'2. Lamanya antara 641-960 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.2']:
                            dat = result['II.M.2'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.2'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.2',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.2'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.3' in result and any(result['II.M.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'3. Lamanya antara 481-640 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.3']:
                            dat = result['II.M.3'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.3'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.3',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.3'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.4' in result and any(result['II.M.4']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.4'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'4. Lamanya antara 161-480 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.4']:
                            dat = result['II.M.4'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.4'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.4',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.4'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.5' in result and any(result['II.M.5']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.5'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'5. Lamanya antara 81-160 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.5']:
                            dat = result['II.M.5'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.5'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.5',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.5'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.6' in result and any(result['II.M.6']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.6'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'6. Lamanya antara 31-80 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.6']:
                            dat = result['II.M.6'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.6'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.6',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.6'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


                if 'II.M.7' in result and any(result['II.M.7']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['II.M.7'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    no = 1
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'7. Lamanya antara 10-30 jam',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    current_row2 = current_row2 + 1
                    start_code = current_row2

                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['II.M.7']:
                            dat = result['II.M.7'][sem]
                    #=============================================================
                        #for period,lines in result['II.M.7'].items():
                            if len(dat) > 1:
                                sheet2.merge_range('J' + str(current_row2) + ':J' + str(current_row2 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet2.write('J' + str(current_row2),getSmt(sem),fmt_box)
                            
                            i = 1
                            for line in dat:
                                sheet2.set_row(current_row2-1,30)
                                sheet2.write('B' + str(current_row2),no,fmt_box)
                                sheet2.merge_range('C' + str(current_row2) + ':I' + str(current_row2),line.name,fmt_box)
                                sheet2.write('L' + str(current_row2),line.volume,fmt_box)
                                sheet2.write('M' + str(current_row2),line.score_max,fmt_box)
                                sheet2.write('N' + str(current_row2),'=L' + str(current_row2) +'*M' + str(current_row2),fmt_box)
                                sheet2.write('O' + str(current_row2),line.note,fmt_box)
                                no += 1
                                i += 1
                                current_row2 = current_row2 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet2.write(x + str(current_row2),'',fmt_box)
                    sheet2.merge_range('B' + str(current_row2) + ':I' + str(current_row2),'Total II.M.7',fmt_box)
                    sheet2.write('N' + str(current_row2),'=SUM(N' + str(start_code) + ':N' + str(current_row2-1) + ')',fmt_box)
                    total['II.M.7'] = '=Lamp.2!N' + str(current_row2)
                    no += 1
                    current_row2 = current_row2 + 1


        #sheet Lamp 3
        sheet3.set_column('A:A',3.5)
        sheet3.set_column('B:F',1.5)
        sheet3.set_column('G:I',7)
        sheet3.set_column('J:J',11)
        sheet3.set_column('K:K',8.2)
        sheet3.set_column('L:L',7)
        sheet3.set_column('M:M',5)
        sheet3.set_column('N:N',7.5)
        sheet3.set_row(0,6.75)
        sheet3.write('K2','Lampiran III:', fmt_wrap)
        sheet3.set_row(1,122.25)
        sheet3.merge_range('L2:O2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet3.merge_range('A6:O6','SURAT PERNYATAAN',fmt_headercenter)
        sheet3.merge_range('A7:O7','MELAKSANAKAN PENELITIAN',fmt_headercenter)
        sheet3.write('A9','Yang bertanda tangan di bawah ini:')
        sheet3.set_row(9,6)
        sheet3.write('C11','Nama')
        sheet3.write('C12','NIP')
        sheet3.write('C13','Pangkat/Golongan Ruang/TMT')
        sheet3.write('C14','Jabatan')
        sheet3.write('C15','Unit Kerja')
        sheet3.write('J11',': ' + conf_wds_name)
        sheet3.write('J12',': ' + conf_wds_nip)
        sheet3.write('J13',': ' + conf_wds_pangkat)
        sheet3.write('J14',': Wakil Dekan Bidang Sumberdaya')
        sheet3.write('J15',': ' + conf_school)
        sheet3.set_row(15,6)
        sheet3.write('A17','Menyatakan bahwa:')
        sheet3.set_row(17,6)
        sheet3.write('C19','Nama')
        sheet3.write('C20','NIP')
        sheet3.write('C21','Pangkat/Golongan Ruang/TMT')
        sheet3.write('C22','Jabatan')
        sheet3.write('C23','Unit Kerja')
        sheet3.write('J19',': ' + dupak.employee_id.name)
        sheet3.write('J20',': ' + dupak.employee_id.nip_new)
        sheet3.write('J21',': ' + dupak.pangkat)
        sheet3.write('J22',': ' + dupak.jabatan)
        sheet3.write('J23',': ' + conf_school)
        sheet3.write('A25','Telah melaksanakan penelitian sebagai berikut:')
        sheet3.write('A27','No.',fmt_columnheader)
        sheet3.merge_range('B27:I27','Uraian Kegiatan',fmt_columnheader)
        sheet3.write('J27','Tanggal',fmt_columnheader)
        sheet3.write('K27','Satuan Hasil',fmt_columnheader)
        sheet3.write('L27','Jumlah Volume Kegiatan',fmt_columnheader)
        sheet3.write('M27','Angka Kredit',fmt_columnheader)
        sheet3.write('N27','Jumlah Angka Kredit',fmt_columnheader)
        sheet3.write('O27','Keterangan/Bukti Fisik',fmt_columnheader)
        sheet3.write('A28','1.',fmt_centerbox)
        sheet3.merge_range('B28:I28','2.',fmt_centerbox)
        sheet3.write('J28','3.',fmt_centerbox)
        sheet3.write('K28','4.',fmt_centerbox)
        sheet3.write('L28','5.',fmt_centerbox)
        sheet3.write('M28','6.',fmt_centerbox)
        sheet3.write('N28','7.',fmt_centerbox)
        sheet3.write('O28','8.',fmt_centerbox)
        current_row3 = 29


        if any(k in result for k in ['III.A.1.a.1','III.A.1.a.2','III.A.1.b.1','III.A.1.b.2','III.A.1.b.3','III.A.1.c.1.a','III.A.1.c.1.b','III.A.1.c.2.a','III.A.1.c.2.b','III.A.1.d','III.A.2','III.B','III.C','III.D.1','III.D.2','III.E.1','III.E.2','III.E.3']):
            sheet3.write('A' + str(current_row3),'III')
            sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'PELAKSANAAN PENELITIAN',fmt_box)
            for x in ['J','K','L','M','N','O']:
                sheet3.write(x + str(current_row3),'',fmt_box)
            current_row3 = current_row3 + 1

            if any(k in result for k in ['III.A.1.a.1','III.A.1.a.2','III.A.1.b.1','III.A.1.b.2','III.A.1.b.3','III.A.1.c.1.a','III.A.1.c.1.b','III.A.1.c.2.a','III.A.1.c.2.b','III.A.1.d','III.A.2']):
                sheet3.write('A' + str(current_row3),'III.A')
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Menghasilkan Karya Ilmiah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                current_row3 = current_row3 + 1

                if any(k in result for k in ['III.A.1.a.1','III.A.1.a.2','III.A.1.b.1','III.A.1.b.2','III.A.1.b.3','III.A.1.c.1.a','III.A.1.c.1.b','III.A.1.c.2.a','III.A.1.c.2.b','III.A.1.d']):
                    sheet3.set_row(current_row3-1,30)
                    sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),'1. Hasil penelitian atau hasil pemikiran yang dipublikasikan',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1

                    if any(k in result for k in ['III.A.1.a.1','III.A.1.a.2']):
                        sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'a. Dalam Bentuk :',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet3.write(x + str(current_row3),'',fmt_box)
                        current_row3 = current_row3 + 1
                        
                        if 'III.A.1.a.1' in result and any(result['III.A.1.a.1']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.a.1'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'1. Monograf, tiap monograf',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3
                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.a.1']:
                                    dat = result['III.A.1.a.1'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.a.1'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet3.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),no,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.a.1',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.a.1'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                        if 'III.A.1.a.2' in result and any(result['III.A.1.a.2']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.a.2'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'2. Buku referensi, tiap buku',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3
                            no = 1

                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.a.2']:
                                    dat = result['III.A.1.a.2'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.a.2'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet3.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),no,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.a.2',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.a.2'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                    if any(k in result for k in ['III.A.1.b.1','III.A.1.b.2','III.A.1.b.3']):
                        sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'b. Jurnal Ilmiah',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet3.write(x + str(current_row3),'',fmt_box)
                        current_row3 = current_row3 + 1
                        
                        if 'III.A.1.b.1' in result and any(result['III.A.1.b.1']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.b.1'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'1. Dalam Jurnal Ilmiah Internasional',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3
                            no = 1

                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.b.1']:
                                    dat = result['III.A.1.b.1'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.b.1'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet3.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),no,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.b.1',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.b.1'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                        if 'III.A.1.b.2' in result and any(result['III.A.1.b.2']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.b.2'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'2. Dalam Jurnal Nasional Terakreditasi',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3
                            no = 1

                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.b.2']:
                                    dat = result['III.A.1.b.2'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.b.2'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet3.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),no,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.b.2',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.b.2'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                        if 'III.A.1.b.3' in result and any(result['III.A.1.b.3']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.b.3'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'3. Dalam Jurnal Nasional tidak Terakreditasi',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3
                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.b.3']:
                                    dat = result['III.A.1.b.3'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.b.3'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet2.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),no,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.b.3',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.b.3'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                    if any(k in result for k in ['III.A.1.c.1.a','III.A.1.c.1.b','III.A.1.c.2.a','III.A.1.c.2.b']):
                        sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'c. Seminar',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet3.write(x + str(current_row3),'',fmt_box)
                        current_row3 = current_row3 + 1
                        
                        if any(k in result for k in ['III.A.1.c.1.a','III.A.1.c.1.b']):
                            sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'1. Disajikan tingkat:',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1

                            if 'III.A.1.c.1.a' in result and any(result['III.A.1.c.1.a']):
                                #======================revisi idris==============================================
                                dumm = []
                                for key,value in result['III.A.1.c.1.a'].items():
                                    dumm.append(key)
                                semester = sorted(set(dumm), key=getSort)
                                #=================================================================================
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'a. Internasional',fmt_box)
                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                current_row3 = current_row3 + 1
                                start_code = current_row3
                                no = 1
                                #=====================revisi==================================
                                for sem in semester:
                                    if sem in result['III.A.1.c.1.a']:
                                        dat = result['III.A.1.c.1.a'][sem]
                                #=============================================================
                                    #for period,lines in result['III.A.1.c.1.a'].items():
                                        if len(dat) > 1:
                                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                        else:
                                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                        
                                        i = 1
                                        for line in dat:
                                            sheet3.set_row(current_row3-1,162)
                                            sheet3.write('E' + str(current_row3),no,fmt_box)
                                            sheet3.merge_range('F' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                            i += 1
                                            no += 1
                                            current_row3 = current_row3 + 1

                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.c.1.a',fmt_box)
                                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                                total['III.A.1.c.1.a'] = '=Lamp.3!N' + str(current_row3)
                                current_row3 = current_row3 + 1


                            if 'III.A.1.c.1.b' in result and any(result['III.A.1.c.1.b']):
                                #======================revisi idris==============================================
                                dumm = []
                                for key,value in result['III.A.1.c.1.b'].items():
                                    dumm.append(key)
                                semester = sorted(set(dumm), key=getSort)
                                #=================================================================================
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'b. Nasional',fmt_box)
                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                current_row3 = current_row3 + 1
                                start_code = current_row3

                                no = 1
                                #=====================revisi==================================
                                for sem in semester:
                                    if sem in result['III.A.1.c.1.b']:
                                        dat = result['III.A.1.c.1.b'][sem]
                                #=============================================================
                                    #for period,lines in result['III.A.1.c.1.b'].items():
                                        if len(dat) > 1:
                                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                        else:
                                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                        
                                        i = 1
                                        for line in dat:
                                            sheet3.set_row(current_row3-1,162)
                                            sheet3.write('E' + str(current_row3),no,fmt_box)
                                            sheet3.merge_range('F' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                            i += 1
                                            no += 1
                                            current_row3 = current_row3 + 1

                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.c.1.b',fmt_box)
                                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                                total['III.A.1.c.1.b'] = '=Lamp.3!N' + str(current_row3)
                                current_row3 = current_row3 + 1


                        if any(k in result for k in ['III.A.1.c.2.a','III.A.1.c.2.b']):
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'2. Poster tingkat:',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1

                            if 'III.A.1.c.2.a' in result and any(result['III.A.1.c.2.a']):
                                #======================revisi idris==============================================
                                dumm = []
                                for key,value in result['III.A.1.c.2.a'].items():
                                    dumm.append(key)
                                semester = sorted(set(dumm), key=getSort)
                                #=================================================================================
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'a. Internasional',fmt_box)
                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                current_row3 = current_row3 + 1
                                start_code = current_row3

                                no = 1
                                #=====================revisi==================================
                                for sem in semester:
                                    if sem in result['III.A.1.c.2.a']:
                                        dat = result['III.A.1.c.2.a'][sem]
                                #=============================================================
                                    #for period,lines in result['III.A.1.c.2.a'].items():
                                        if len(dat) > 1:
                                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                        else:
                                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                        
                                        i = 1
                                        for line in dat:
                                            sheet3.set_row(current_row3-1,162)
                                            sheet3.write('E' + str(current_row3),no,fmt_box)
                                            sheet3.merge_range('F' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                            i += 1
                                            no += 1
                                            current_row3 = current_row3 + 1

                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.c.2.a',fmt_box)
                                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                                total['III.A.1.c.2.a'] = '=Lamp.3!N' + str(current_row3)
                                current_row3 = current_row3 + 1


                            if 'III.A.1.c.2.b' in result and any(result['III.A.1.c.2.b']):
                                #======================revisi idris==============================================
                                dumm = []
                                for key,value in result['III.A.1.c.2.b'].items():
                                    dumm.append(key)
                                semester = sorted(set(dumm), key=getSort)
                                #=================================================================================
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'b. Nasional',fmt_box)
                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                current_row3 = current_row3 + 1
                                start_code = current_row3

                                no = 1
                                #=====================revisi==================================
                                for sem in semester:
                                    if sem in result['III.A.1.c.2.b']:
                                        dat = result['III.A.1.c.2.b'][sem]
                                #=============================================================
                                    #for period,lines in result['III.A.1.c.2.b'].items():
                                        if len(dat) > 1:
                                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                        else:
                                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                        
                                        i = 1
                                        for line in dat:
                                            sheet3.set_row(current_row3-1,162)
                                            sheet3.write('E' + str(current_row3),no,fmt_box)
                                            sheet3.merge_range('F' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                            i += 1
                                            no += 1
                                            current_row3 = current_row3 + 1

                                for x in ['J','K','L','M','N','O']:
                                    sheet3.write(x + str(current_row3),'',fmt_box)
                                sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.c.2.b',fmt_box)
                                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                                total['III.A.1.c.2.b'] = '=Lamp.3!N' + str(current_row3)
                                current_row3 = current_row3 + 1


                        if 'III.A.1.d' in result and any(result['III.A.1.d']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['III.A.1.d'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'d. Dalam koran/majalah populer/umum',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            current_row3 = current_row3 + 1
                            start_code = current_row3

                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['III.A.1.d']:
                                    dat = result['III.A.1.d'][sem]
                            #=============================================================
                                #for period,lines in result['III.A.1.d'].items():
                                    if len(dat) > 1:
                                        sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                                    else:
                                        sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                                    i = 1
                                    for line in dat:
                                        sheet3.set_row(current_row3-1,162)
                                        sheet3.write('D' + str(current_row3),i,fmt_box)
                                        sheet3.merge_range('E' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                        sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                        sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                        sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                        sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row3 = current_row3 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet3.write(x + str(current_row3),'',fmt_box)
                            sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),'Total III.A.1.d',fmt_box)
                            sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                            total['III.A.1.d'] = '=Lamp.3!N' + str(current_row3)
                            current_row3 = current_row3 + 1


                if 'III.A.2' in result and any(result['III.A.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.A.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.set_row(current_row3-1,30)
                    sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),'2. Hasil penelitian atau hasil pemikiran yang tidak dipublikasikan (tersimpan diperpustakaan perguruan tinggi)',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.A.2']:
                            dat = result['III.A.2'][sem]
                    #=============================================================
                        #for period,lines in result['III.A.2'].items():
                            if len(dat) > 1:
                                sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                           
                            i = 1
                            for line in dat:
                                sheet3.set_row(current_row3-1,162)
                                sheet3.write('C' + str(current_row3),no,fmt_box)
                                sheet3.merge_range('D' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),'Total III.A.2',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.A.2'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1


            if 'III.B' in result and any(result['III.B']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['III.B'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet3.set_row(current_row3-1,30)
                sheet3.write('A' + str(current_row3),'III.B')
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Menerjemahkan/menyadur buku ilmiah (diterbitkan & diedarkan secara nasional)',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                current_row3 = current_row3 + 1
                start_code = current_row3

                no = 1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['III.B']:
                        dat = result['III.B'][sem]
                #=============================================================
                    #for period,lines in result['III.B'].items():
                        if len(dat) > 1:
                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                
                        i = 1
                        for line in dat:
                            sheet3.set_row(current_row3-1,162)
                            sheet3.write('B' + str(current_row3),no,fmt_box)
                            sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row3 = current_row3 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.B',fmt_box)
                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                total['III.B'] = '=Lamp.3!N' + str(current_row3)
                current_row3 = current_row3 + 1
            
            
            if 'III.C' in result and any(result['III.C']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['III.C'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet.set_row(current_row3-1,30)
                sheet3.write('A' + str(current_row3),'III.C')
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Mengedit/menyunting karya ilmiah (diterbitkan & diedarkan secara nasional)',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                current_row3 = current_row3 + 1
                start_code = current_row3

                no = 1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['III.C']:
                        dat = result['III.C'][sem]
                #=============================================================
                    #for period,lines in result['III.C'].items():
                        if len(dat) > 1:
                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                
                        i = 1
                        for line in dat:
                            sheet3.set_row(current_row3-1,162)
                            sheet3.write('B' + str(current_row3),no,fmt_box)
                            sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row3 = current_row3 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.C',fmt_box)
                sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                total['III.C'] = '=Lamp.3!N' + str(current_row3)
                current_row3 = current_row3 + 1


            if any(k in result for k in ['III.D.1','III.D.2']):
                sheet3.set_row(current_row3-1,30)
                sheet3.write('A' + str(current_row3),'III.D')
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Membuat rencana & karya teknologi yg. dipatenkan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                current_row3 = current_row3 + 1
                
                if 'III.D.1' in result and any(result['III.D.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.D.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'1. Internasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.D.1']:
                            dat = result['III.D.1'][sem]
                    #=============================================================
                    #for period,lines in result['III.D.1'].items():
                        if len(dat) > 1:
                            sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                        else:
                            sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                
                        i = 1
                        for line in dat:
                            sheet3.set_row(current_row3-1,162)
                            sheet3.write('B' + str(current_row3),no,fmt_box)
                            sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                            sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                            sheet3.write('M' + str(current_row3),line.score,fmt_box)
                            sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                            sheet3.write('O' + str(current_row3),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.D.1',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.D.1'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1


                if 'III.D.2' in result and any(result['III.D.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.D.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'2. Nasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.D.2']:
                            dat = result['III.D.2'][sem]
                    #=============================================================
                        #for period,lines in result['III.D.2'].items():
                            if len(dat) > 1:
                                sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                            i = 1
                            for line in dat:
                                sheet3.set_row(current_row3-1,162)
                                sheet3.write('B' + str(current_row3),no,fmt_box)
                                sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.D.2',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.D.2'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1


            if any(k in result for k in ['III.E.1','III.E.2','III.E.3']):
                sheet3.set_row(current_row3-1,30)
                sheet3.write('A' + str(current_row3),'III.E')
                sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Membuat rancangan dan karya teknologi, rancangan dan karya seni monumental/seni pertunjukan/karya sastra',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet3.write(x + str(current_row3),'',fmt_box)
                current_row3 = current_row3 + 1
                
                if 'III.E.1' in result and any(result['III.E.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.E.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'1. Tingkat Internasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.E.1']:
                            dat = result['III.E.1'][sem]
                    #=============================================================
                        #for period,lines in result['III.E.1'].items():
                            if len(dat) > 1:
                                sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                            i = 1
                            for line in dat:
                                sheet3.set_row(current_row3-1,162)
                                sheet3.write('B' + str(current_row3),no,fmt_box)
                                sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.E.1',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.E.1'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1


                if 'III.E.2' in result and any(result['III.E.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.E.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'2. Tingkat Nasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.E.2']:
                            dat = result['III.E.2'][sem]
                    #=============================================================
                        #for period,lines in result['III.E.2'].items():
                            if len(dat) > 1:
                                sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                            i = 1
                            for line in dat:
                                sheet3.set_row(current_row3-1,162)
                                sheet3.write('B' + str(current_row3),no,fmt_box)
                                sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.E.2',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.E.2'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1


                if 'III.E.3' in result and any(result['III.E.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['III.E.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'3. Tingkat Lokal',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    current_row3 = current_row3 + 1
                    start_code = current_row3

                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['III.E.3']:
                            dat = result['III.E.3'][sem]
                    #=============================================================
                        #for period,lines in result['III.E.3'].items():
                            if len(dat) > 1:
                                sheet3.merge_range('J' + str(current_row3) + ':J' + str(current_row3 + len(dat) - 1),getSmt(sem),fmt_box)
                            else:
                                sheet3.write('J' + str(current_row3),getSmt(sem),fmt_box)
                                    
                            i = 1
                            for line in dat:
                                sheet3.set_row(current_row3-1,162)
                                sheet3.write('B' + str(current_row3),no,fmt_box)
                                sheet3.merge_range('C' + str(current_row3) + ':I' + str(current_row3),line.name,fmt_box)
                                sheet3.write('L' + str(current_row3),line.volume,fmt_box)
                                sheet3.write('M' + str(current_row3),line.score,fmt_box)
                                sheet3.write('N' + str(current_row3),'=L' + str(current_row3) +'*M' + str(current_row3),fmt_box)
                                sheet3.write('O' + str(current_row3),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row3 = current_row3 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet3.write(x + str(current_row3),'',fmt_box)
                    sheet3.merge_range('B' + str(current_row3) + ':I' + str(current_row3),'Total III.E.3',fmt_box)
                    sheet3.write('N' + str(current_row3),'=SUM(N' + str(start_code) + ':N' + str(current_row3-1) + ')',fmt_box)
                    total['III.E.3'] = '=Lamp.3!N' + str(current_row3)
                    current_row3 = current_row3 + 1



        #sheet Lamp 4
        sheet4.set_column('A:A',3.5)
        sheet4.set_column('B:F',1.5)
        sheet4.set_column('G:I',7)
        sheet4.set_column('J:J',11)
        sheet4.set_column('K:K',8.2)
        sheet4.set_column('L:L',7)
        sheet4.set_column('M:M',5)
        sheet4.set_column('N:N',7.5)
        sheet4.set_row(0,6.75)
        sheet4.write('K2','Lampiran IV:', fmt_wrap)
        sheet4.set_row(1,122.25)
        sheet4.merge_range('L2:O2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet4.merge_range('A6:O6','SURAT PERNYATAAN',fmt_headercenter)
        sheet4.merge_range('A7:O7','MELAKSANAKAN PENGABDIAN KEPADA MASYARAKAT',fmt_headercenter)
        sheet4.write('A9','Yang bertanda tangan di bawah ini:')
        sheet4.set_row(9,6)
        sheet4.write('C11','Nama')
        sheet4.write('C12','NIP')
        sheet4.write('C13','Pangkat/Golongan Ruang/TMT')
        sheet4.write('C14','Jabatan')
        sheet4.write('C15','Unit Kerja')
        sheet4.write('J11',': ' + conf_wds_name)
        sheet4.write('J12',': ' + conf_wds_nip)
        sheet4.write('J13',': ' + conf_wds_pangkat)
        sheet4.write('J14',': Wakil Dekan Bidang Sumberdaya')
        sheet4.write('J15',': ' + conf_school)
        sheet4.set_row(15,6)
        sheet4.write('A17','Menyatakan bahwa:')
        sheet4.set_row(17,6)
        sheet4.write('C19','Nama')
        sheet4.write('C20','NIP')
        sheet4.write('C21','Pangkat/Golongan Ruang/TMT')
        sheet4.write('C22','Jabatan')
        sheet4.write('C23','Unit Kerja')
        sheet4.write('J19',': ' + dupak.employee_id.name)
        sheet4.write('J20',': ' + dupak.employee_id.nip_new)
        sheet4.write('J21',': ' + dupak.pangkat)
        sheet4.write('J22',': ' + dupak.jabatan)
        sheet4.write('J23',': ' + conf_school)
        sheet4.write('A25','Telah melaksanakan pengabdian kepada masyarakat sebagai berikut:')
        sheet4.write('A27','No.',fmt_columnheader)
        sheet4.merge_range('B27:I27','Uraian Kegiatan',fmt_columnheader)
        sheet4.write('J27','Tanggal',fmt_columnheader)
        sheet4.write('K27','Satuan Hasil',fmt_columnheader)
        sheet4.write('L27','Jumlah Volume Kegiatan',fmt_columnheader)
        sheet4.write('M27','Angka Kredit',fmt_columnheader)
        sheet4.write('N27','Jumlah Angka Kredit',fmt_columnheader)
        sheet4.write('O27','Keterangan/Bukti Fisik',fmt_columnheader)
        sheet4.write('A28','1.',fmt_centerbox)
        sheet4.merge_range('B28:I28','2.',fmt_centerbox)
        sheet4.write('J28','3.',fmt_centerbox)
        sheet4.write('K28','4.',fmt_centerbox)
        sheet4.write('L28','5.',fmt_centerbox)
        sheet4.write('M28','6.',fmt_centerbox)
        sheet4.write('N28','7.',fmt_centerbox)
        sheet4.write('O28','8.',fmt_centerbox)
        current_row4 = 29


        if any(k in result for k in ['IV.A','IV.B','IV.C.1.a.1','IV.C.1.a.2','IV.C.1.a.3','IV.C.1.b.1','IV.C.1.b.2','IV.C.1.b.3','IV.C.2','IV.D.1','IV.D.2','IV.D.3','IV.E']):
            sheet4.write('A' + str(current_row4),'IV')
            sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'PELAKSANAAN PENGABDIAN KEPADA MASYARAKAT',fmt_box)
            for x in ['J','K','L','M','N','O']:
                sheet4.write(x + str(current_row4),'',fmt_box)
            current_row4 = current_row4 + 1

            if 'IV.A' in result and any(result['IV.A']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['IV.A'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet4.set_row(current_row4-1,40)
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Menduduki jabatan pimpinan pada lembaga pemerintahan/pejabat Negara yang harus dibebaskan dari jabatan organiknya',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                current_row4 = current_row4 + 1
                start_code = current_row4

                no = 1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['IV.A']:
                        dat = result['IV.A'][sem]
                #=============================================================
                    #for period,lines in result['IV.A'].items():
                        if len(dat) > 1:
                            sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                        else:
                            sheet4.write('J' + str(current_row4),sem,fmt_box)
                            
                        i = 1
                        for line in dat:
                            sheet4.set_row(current_row4-1,40)
                            sheet4.write('B' + str(current_row4),no,fmt_box)
                            sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                            sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                            sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                            sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                            sheet4.write('O' + str(current_row4),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row4 = current_row4 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.A',fmt_box)
                sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                total['IV.A'] = '=Lamp.4!N' + str(current_row4)
                current_row4 = current_row4 + 1

            
            if 'IV.B' in result and any(result['IV.B']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['IV.B'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet4.set_row(current_row4-1,40)
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Melaksanakan pengembangan hasil pendidikan dan penelitian yang dapat dimanfaatkan oleh masyarakat',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                current_row4 = current_row4 + 1
                start_code = current_row4

                no = 1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['IV.B']:
                        dat = result['IV.B'][sem]
                #=============================================================
                    #for period,lines in result['IV.A'].items():
                        if len(dat) > 1:
                            sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                        else:
                            sheet4.write('J' + str(current_row4),sem,fmt_box)
                            
                        i = 1
                        for line in dat:
                            sheet4.set_row(current_row4-1,40)
                            sheet4.write('B' + str(current_row4),no,fmt_box)
                            sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                            sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                            sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                            sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                            sheet4.write('O' + str(current_row4),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row4 = current_row4 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.B',fmt_box)
                sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                total['IV.B'] = '=Lamp.4!N' + str(current_row4)
                current_row4 = current_row4 + 1


            if any(k in result for k in ['IV.C.1.a.1','IV.C.1.a.2','IV.C.1.a.3','IV.C.1.b.1','IV.C.1.b.2','IV.C.1.b.3','IV.C.2']):
                sheet4.set_row(current_row4-1,30)
                sheet4.write('A' + str(current_row4),'IV.C')
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Memberi latihan/penyuluhan/penataran/ceramah pada masyarakat',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                current_row4 = current_row4 + 1

                if any(k in result for k in ['IV.C.1.a.1','IV.C.1.a.2','IV.C.1.a.3','IV.C.1.b.1','IV.C.1.b.2','IV.C.1.b.3']):
                    sheet4.write('B' + str(current_row4),'1.')
                    sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),'Terjadwal/terprogram',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    current_row4 = current_row4 + 1

                    if any(k in result for k in ['IV.C.1.a.1','IV.C.1.a.2','IV.C.1.a.3']):
                        sheet4.write('C' + str(current_row4),'a.')
                        sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Dalam 1 semester atau lebih',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet4.write(x + str(current_row4),'',fmt_box)
                        current_row4 = current_row4 + 1

                        if 'IV.C.1.a.1' in result and any(result['IV.C.1.a.1']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.a.1'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'1. Tingkat Internasional',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4

                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.a.1']:
                                    dat = result['IV.C.1.a.1'][sem]
                            #=============================================================
                                #for period,lines in result['IV.C.1.a.1'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.a.1',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.a.1'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                        if 'IV.C.1.a.2' in result and any(result['IV.C.1.a.2']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.a.2'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'2. Tingkat Nasional',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4
                            
                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.a.2']:
                                    dat = result['IV.C.1.a.2'][sem]
                            #=============================================================
                               # for period,lines in result['IV.C.1.a.2'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.a.2',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.a.2'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                        if 'IV.C.1.a.3' in result and any(result['IV.C.1.a.3']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.a.3'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'3. Tingkat Lokal',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4

                            no=1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.a.3']:
                                    dat = result['IV.C.1.a.3'][sem]
                            #=============================================================
                                #for period,lines in result['IV.C.1.a.3'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.a.3',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.a.3'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                    if any(k in result for k in ['IV.C.1.b.1','IV.C.1.b.2','IV.C.1.b.3']):
                        sheet4.set_row(current_row4-1,20)
                        sheet4.write('C' + str(current_row4),'b.')
                        sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Kurang dari 1 semester dan minimal 1 bulan',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet4.write(x + str(current_row4),'',fmt_box)
                        current_row4 = current_row4 + 1

                        if 'IV.C.1.b.1' in result and any(result['IV.C.1.b.1']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.b.1'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'1. Tingkat Internasional',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4
##########################belum dirubah#####################################################
############################################################################################
############################################################################################
                            no =  1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.b.1']:
                                    dat = result['IV.C.1.b.1'][sem]
                            #=============================================================
                                #for period,lines in result['IV.C.1.b.1'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.b.1',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.b.1'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                        if 'IV.C.1.b.2' in result and any(result['IV.C.1.b.2']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.b.2'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'2. Tingkat Nasional',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4

                            no = 1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.b.2']:
                                    dat = result['IV.C.1.b.2'][sem]
                            #=============================================================
                                #for period,lines in result['IV.C.1.b.2'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.b.2',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.b.2'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                        if 'IV.C.1.b.3' in result and any(result['IV.C.1.b.3']):
                            #======================revisi idris==============================================
                            dumm = []
                            for key,value in result['IV.C.1.b.3'].items():
                                dumm.append(key)
                            semester = sorted(set(dumm), key=getSort)
                            #=================================================================================
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'3. Tingkat Lokal',fmt_box)
                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            current_row4 = current_row4 + 1
                            start_code = current_row4

                            no =  1
                            #=====================revisi==================================
                            for sem in semester:
                                if sem in result['IV.C.1.b.3']:
                                    dat = result['IV.C.1.b.3'][sem]
                            #=============================================================
                                #for period,lines in result['IV.C.1.b.3'].items():
                                    if len(dat) > 1:
                                        sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                                    else:
                                        sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                                    i = 1
                                    for line in dat:
                                        sheet4.set_row(current_row4-1,40)
                                        sheet4.write('D' + str(current_row4),no,fmt_box)
                                        sheet4.merge_range('E' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                        sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                        sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                        sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                        sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                        i += 1
                                        no += 1
                                        current_row4 = current_row4 + 1

                            for x in ['J','K','L','M','N','O']:
                                sheet4.write(x + str(current_row4),'',fmt_box)
                            sheet4.merge_range('D' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.1.b.3',fmt_box)
                            sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                            total['IV.C.1.b.3'] = '=Lamp.4!N' + str(current_row4)
                            current_row4 = current_row4 + 1


                if 'IV.C.2' in result and any(result['IV.C.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['IV.C.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'2. Insidental',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    current_row4 = current_row4 + 1
                    start_code = current_row4
                    
                    no = 1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['IV.C.2']:
                            dat = result['IV.C.2'][sem]
                    #=============================================================
                        #for period,lines in result['IV.C.2'].items():
                            if len(dat) > 1:
                                sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet4.write('J' + str(current_row4),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet4.set_row(current_row4-1,40)
                                sheet4.write('B' + str(current_row4),no,fmt_box)
                                sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row4 = current_row4 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.C.2',fmt_box)
                    sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                    total['IV.C.2'] = '=Lamp.4!N' + str(current_row4)
                    current_row4 = current_row4 + 1


            if any(k in result for k in ['IV.D.1','IV.D.2','IV.D.3']):
                sheet4.set_row(current_row4-1,30)
                sheet4.write('A' + str(current_row4),'IV.D')
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Memberi pelayanan kepada masyarakat atau kegiatan lain yang menunjang pelaksanaan tugas umum pemerintahan dan pembangunan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                current_row4 = current_row4 + 1

                if 'IV.D.1' in result and any(result['IV.D.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['IV.D.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'1. Berdasarkan keahlian',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    current_row4 = current_row4 + 1
                    start_code = current_row4

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['IV.D.1']:
                            dat = result['IV.D.1'][sem]
                    #=============================================================
                        #for period,lines in result['IV.D.1'].items():
                            if len(dat) > 1:
                                sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet4.write('J' + str(current_row4),sem,fmt_box)
                                
                            i = 1
                            for line in dat:
                                sheet4.set_row(current_row4-1,40)
                                sheet4.write('B' + str(current_row4),no,fmt_box)
                                sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row4 = current_row4 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.D.1',fmt_box)
                    sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                    total['IV.D.1'] = '=Lamp.4!N' + str(current_row4)
                    current_row4 = current_row4 + 1


                if 'IV.D.2' in result and any(result['IV.D.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['IV.D.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'2. Berdasarkan penugasan lembaga PT',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    current_row4 = current_row4 + 1
                    start_code = current_row4

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['IV.D.2']:
                            dat = result['IV.D.2'][sem]
                    #=============================================================
                        #for period,lines in result['IV.D.2'].items():
                            if len(dat) > 1:
                                sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet4.write('J' + str(current_row4),sem,fmt_box)
                                
                            i = 1
                            for line in dat:
                                sheet4.set_row(current_row4-1,40)
                                sheet4.write('B' + str(current_row4),no,fmt_box)
                                sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row4 = current_row4 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.D.2',fmt_box)
                    sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                    total['IV.D.2'] = '=Lamp.4!N' + str(current_row4)
                    current_row4 = current_row4 + 1


                if 'IV.D.3' in result and any(result['IV.D.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['IV.D.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'3. Berdasarkan fungsi/jabatan',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    current_row4 = current_row4 + 1
                    start_code = current_row4

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['IV.D.3']:
                            dat = result['IV.D.3'][sem]
                    #=============================================================
                        #for period,lines in result['IV.D.3'].items():
                            if len(dat) > 1:
                                sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet4.write('J' + str(current_row4),sem,fmt_box)
                                
                            i = 1
                            for line in dat:
                                sheet4.set_row(current_row4-1,40)
                                sheet4.write('B' + str(current_row4),no,fmt_box)
                                sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                                sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                                sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                                sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                                sheet4.write('O' + str(current_row4),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row4 = current_row4 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet4.write(x + str(current_row4),'',fmt_box)
                    sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.D.3',fmt_box)
                    sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                    total['IV.D.3'] = '=Lamp.4!N' + str(current_row4)
                    current_row4 = current_row4 + 1


            if 'IV.E' in result and any(result['IV.E']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['IV.E'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet4.set_row(current_row4-1,30)
                sheet4.write('A' + str(current_row4),'IV.E')
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Membuat/menulis karya pengabdian pada masyarakat yang tidak dipublikasikan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                current_row4 = current_row4 + 1
                start_code = current_row4

                no =  1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['IV.E']:
                        dat = result['IV.E'][sem]
                #=============================================================
                    #for period,lines in result['IV.E'].items():
                        if len(dat) > 1:
                            sheet4.merge_range('J' + str(current_row4) + ':J' + str(current_row4 + len(dat) - 1),sem,fmt_box)
                        else:
                            sheet4.write('J' + str(current_row4),sem,fmt_box)
                            
                        i = 1
                        for line in dat:
                            sheet4.set_row(current_row4-1,40)
                            sheet4.write('B' + str(current_row4),no,fmt_box)
                            sheet4.merge_range('C' + str(current_row4) + ':I' + str(current_row4),line.name,fmt_box)
                            sheet4.write('L' + str(current_row4),line.volume,fmt_box)
                            sheet4.write('M' + str(current_row4),line.score_max,fmt_box)
                            sheet4.write('N' + str(current_row4),'=L' + str(current_row4) +'*M' + str(current_row4),fmt_box)
                            sheet4.write('O' + str(current_row4),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row4 = current_row4 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet4.write(x + str(current_row4),'',fmt_box)
                sheet4.merge_range('B' + str(current_row4) + ':I' + str(current_row4),'Total IV.E',fmt_box)
                sheet4.write('N' + str(current_row4),'=SUM(N' + str(start_code) + ':N' + str(current_row4-1) + ')',fmt_box)
                total['IV.E'] = '=Lamp.4!N' + str(current_row4)
                current_row4 = current_row4 + 1



        #sheet Lamp 5
        sheet5.set_column('A:A',3.5)
        sheet5.set_column('B:F',1.5)
        sheet5.set_column('G:I',7)
        sheet5.set_column('J:J',11)
        sheet5.set_column('K:K',8.2)
        sheet5.set_column('L:L',7)
        sheet5.set_column('M:M',5)
        sheet5.set_column('N:N',7.5)
        sheet5.set_row(0,6.75)
        sheet5.write('K2','Lampiran V:', fmt_wrap)
        sheet5.set_row(1,122.25)
        sheet5.merge_range('L2:O2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet5.merge_range('A6:O6','SURAT PERNYATAAN',fmt_headercenter)
        sheet5.merge_range('A7:O7','MELAKSANAKAN KEGIATAN PENUNJANG TRI DHARMA PERGURUAN TINGGI',fmt_headercenter)
        sheet5.write('A9','Yang bertanda tangan di bawah ini:')
        sheet5.set_row(9,6)
        sheet5.write('C11','Nama')
        sheet5.write('C12','NIP')
        sheet5.write('C13','Pangkat/Golongan Ruang/TMT')
        sheet5.write('C14','Jabatan')
        sheet5.write('C15','Unit Kerja')
        sheet5.write('J11',': ' + conf_wds_name)
        sheet5.write('J12',': ' + conf_wds_nip)
        sheet5.write('J13',': ' + conf_wds_pangkat)
        sheet5.write('J14',': Wakil Dekan Bidang Sumberdaya')
        sheet5.write('J15',': ' + conf_school)
        sheet5.set_row(15,6)
        sheet5.write('A17','Menyatakan bahwa:')
        sheet5.set_row(17,6)
        sheet5.write('C19','Nama')
        sheet5.write('C20','NIP')
        sheet5.write('C21','Pangkat/Golongan Ruang/TMT')
        sheet5.write('C22','Jabatan')
        sheet5.write('C23','Unit Kerja')
        sheet5.write('J19',': ' + dupak.employee_id.name)
        sheet5.write('J20',': ' + dupak.employee_id.nip_new)
        sheet5.write('J21',': ' + dupak.pangkat)
        sheet5.write('J22',': ' + dupak.jabatan)
        sheet5.write('J23',': ' + conf_school)
        sheet5.write('A25','Telah melaksanakan kegiatan penunjang Dosen sebagai berikut:')
        sheet5.write('A27','No.',fmt_columnheader)
        sheet5.merge_range('B27:I27','Uraian Kegiatan',fmt_columnheader)
        sheet5.write('J27','Tanggal',fmt_columnheader)
        sheet5.write('K27','Satuan Hasil',fmt_columnheader)
        sheet5.write('L27','Jumlah Volume Kegiatan',fmt_columnheader)
        sheet5.write('M27','Angka Kredit',fmt_columnheader)
        sheet5.write('N27','Jumlah Angka Kredit',fmt_columnheader)
        sheet5.write('O27','Keterangan/Bukti Fisik',fmt_columnheader)
        sheet5.write('A28','1.',fmt_centerbox)
        sheet5.merge_range('B28:I28','2.',fmt_centerbox)
        sheet5.write('J28','3.',fmt_centerbox)
        sheet5.write('K28','4.',fmt_centerbox)
        sheet5.write('L28','5.',fmt_centerbox)
        sheet5.write('M28','6.',fmt_centerbox)
        sheet5.write('N28','7.',fmt_centerbox)
        sheet5.write('O28','8.',fmt_centerbox)
        current_row5 = 29


        if any(k in result for k in ['V.A.1','V.A.2','V.B.1.a','V.B.1.b','V.B.2.a','V.B.2.b','V.C.1.a','V.C.1.b','V.C.1.c','V.C.2.a','V.C.2.b','V.C.2.c','V.D','V.E.1','V.E.2','V.F.1.a','V.F.1.b','V.F.2.a','V.F.2.b','V.G.1.a','V.G.1.b','V.G.1.c','V.G.2.a','V.G.2.b','V.G.2.c','V.H.1','V.H.2','V.H.3','V.I.1','V.I.2','V.I.3','V.J']):
            sheet5.write('A' + str(current_row5),'V')
            sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'PENUNJANG KEGIATAN AKADEMIK DOSEN',fmt_box)
            for x in ['J','K','L','M','N','O']:
                sheet5.write(x + str(current_row5),'',fmt_box)
            current_row5 = current_row5 + 1
            
            if any(k in result for k in ['V.A.1','V.A.2']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.A')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menjadi anggota dalam suatu Panitia/Badan pada Perguruan Tinggi',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1

                if 'V.A.1' in result and any(result['V.A.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.A.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.set_row(current_row5-1,30)
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'1. Sebagai Ketua/Wakil Ketua merangkap anggota',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.A.1']:
                            dat = result['V.A.1'][sem]
                    #=============================================================
                        #for period,lines in result['V.A.1'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('C' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.A.1',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.A.1'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.A.2' in result and any(result['V.A.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.A.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'2. Sebagai anggota',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.A.2']:
                            dat = result['V.A.2'][sem]
                    #=============================================================
                        #for period,lines in result['V.A.2'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('C' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.A.2',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.A.2'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


            if any(k in result for k in ['V.B.1.a','V.B.1.b','V.B.2.a','V.B.2.b']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.B')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menjadi anggota panitia/badan pada lembaga pemerintah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                
                if any(k in result for k in ['V.B.1.a','V.B.1.b']):
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'1. Panitia Pusat',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.B.1.a' in result and any(result['V.B.1.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.B.1.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'a. Ketua/Wakil Ketua',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.B.1.a']:
                                dat = result['V.B.1.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.B.1.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.B.1.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.B.1.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.B.1.b' in result and any(result['V.B.1.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.B.1.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'b. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.B.1.b']:
                                dat = result['V.B.1.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.B.1.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.B.1.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.B.1.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                if any(k in result for k in ['V.B.2.a','V.B.2.b']):
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'2. Panitia Daerah',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.B.2.a' in result and any(result['V.B.2.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.B.2.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'a. Ketua/Wakil Ketua',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.B.2.a']:
                                dat = result['V.B.2.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.B.2.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.B.2.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.B.2.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.B.2.b' in result and any(result['V.B.2.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.B.2.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'b. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.B.2.b']:
                                dat = result['V.B.2.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.B.2.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.B.2.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.B.2.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


            if any(k in result for k in ['V.C.1.a','V.C.1.b','V.C.1.c','V.C.2.a','V.C.2.b','V.C.2.c']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.C')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menjadi anggota organisasi profesi dosen',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                
                if any(k in result for k in ['V.C.1.a','V.C.1.b','V.C.1.c']):
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'1. Tingkat Internasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.C.1.a' in result and any(result['V.C.1.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.1.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'a. Pengurus',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.1.a']:
                                dat = result['V.C.1.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.1.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.1.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.1.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.C.1.b' in result and any(result['V.C.1.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.1.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'b. Anggota atas permintaan',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.1.b']:
                                dat = result['V.C.1.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.1.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.1.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.1.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.C.1.c' in result and any(result['V.C.1.c']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.1.c'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'c. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.1.c']:
                                dat = result['V.C.1.c'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.1.c'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.1.c',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.1.c'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                if any(k in result for k in ['V.C.2.a','V.C.2.b','V.C.2.c']):
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'2. Tingkat Nasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.C.2.a' in result and any(result['V.C.2.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.2.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'a. Pengurus',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.2.a']:
                                dat = result['V.C.2.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.2.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.2.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.2.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.C.2.b' in result and any(result['V.C.2.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.2.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'b. Anggota atas permintaan',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.2.b']:
                                dat = result['V.C.2.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.2.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.2.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.2.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.C.2.c' in result and any(result['V.C.2.c']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.C.2.c'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'c. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.C.2.c']:
                                dat = result['V.C.2.c'][sem]
                        #=============================================================
                            #for period,lines in result['V.C.2.c'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('D' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('E' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),'Total V.C.2.c',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.C.2.c'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


            if 'V.D' in result and any(result['V.D']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['V.D'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet5.write('A' + str(current_row5),'V.D')               
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Mewakili Perguruan Tinggi/Lembaga Pemerintah duduk dalam panitia antar lembaga',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                start_code = current_row5

                no =  1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['V.D']:
                        dat = result['V.D'][sem]
                #=============================================================
                    #for period,lines in result['V.D'].items():
                        if len(dat) > 1:
                            sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                        else:
                            sheet5.write('J' + str(current_row5),sem,fmt_box)
                                    
                        i = 1
                        for line in dat:
                            sheet5.set_row(current_row5-1,30)
                            sheet5.write('B' + str(current_row5),no,fmt_box)
                            sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                            sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                            sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                            sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                            sheet5.write('O' + str(current_row5),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row5 = current_row5 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.D',fmt_box)
                sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                total['V.D'] = '=Lamp.5!N' + str(current_row5)
                current_row5 = current_row5 + 1


            if any(k in result for k in ['V.E.1','V.E.2']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.E')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menjadi anggota delegasi nasional ke pertemuan Internasional',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1

                if 'V.E.1' in result and any(result['V.E.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.E.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'1. Ketua Delegasi',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.E.1']:
                            dat = result['V.E.1'][sem]
                    #=============================================================
                        #for period,lines in result['V.E.1'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('C' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.E.1',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.E.1'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.E.2' in result and any(result['V.E.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.E.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'2. Anggota Delegasi',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.E.2']:
                            dat = result['V.E.2'][sem]
                    #=============================================================
                        #for period,lines in result['V.E.2'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.write('C' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.E.2',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.E.2'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1



            if any(k in result for k in ['V.F.1.a','V.F.1.b','V.F.2.a','V.F.2.b']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.F')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Berperan serta aktif dalam pertemuan ilmiah',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                
                if any(k in result for k in ['V.F.1.a','V.F.1.b']):
                    sheet5.set_row(current_row5-1,30)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'1. Tingkat internasional/nasional/regional sebagai',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.F.1.a' in result and any(result['V.F.1.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.F.1.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'a. Ketua',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.F.1.a']:
                                dat = result['V.F.1.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.F.1.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.F.1.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.F.1.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.F.1.b' in result and any(result['V.F.1.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.F.1.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'b. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.F.1.b']:
                                dat = result['V.F.1.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.F.1.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.F.1.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.F.1.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                if any(k in result for k in ['V.F.2.a','V.F.2.b']):
                    sheet5.set_row(current_row5-1,30)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'2. Di lingkungan perguruan tinggi sendiri',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.F.2.a' in result and any(result['V.F.2.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.F.2.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'a. Ketua',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.F.2.a']:
                                dat = result['V.F.2.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.F.2.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.F.2.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.F.2.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.F.2.b' in result and any(result['V.F.2.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.F.2.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'b. Anggota',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.F.2.b']:
                                dat = result['V.F.2.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.F.2.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.F.2.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.F.2.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


            if any(k in result for k in ['V.G.1.a','V.G.1.b','V.G.1.c','V.G.2.a','V.G.2.b','V.G.2.c']):
                sheet5.write('A' + str(current_row5),'V.G')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Mendapat tanda jasa/penghargaan',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                
                if any(k in result for k in ['V.G.1.a','V.G.1.b','V.G.1.c']):
                    sheet5.set_row(current_row5-1,30)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'1. Penghargaan/tanda jasa Satyalancana Karya Satya',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.G.1.a' in result and any(result['V.G.1.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.1.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'a. 30 (tiga puluh) tahun',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.1.a']:
                                dat = result['V.G.1.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.1.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.1.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.1.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.G.1.b' in result and any(result['V.G.1.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.1.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'b. 20 (dua puluh) tahun',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.1.b']:
                                dat = result['V.G.1.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.1.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.1.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.1.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.G.1.c' in result and any(result['V.G.1.c']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.1.c'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'c. 10 (sepuluh) tahun',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.1.c']:
                                dat = result['V.G.1.c'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.1.c'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.1.c',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.1.c'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                if any(k in result for k in ['V.G.2.a','V.G.2.b','V.G.2.c']):
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'2. Memperoleh penghargaan lainnya',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1

                    if 'V.G.2.a' in result and any(result['V.G.2.a']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.2.a'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'a. Tingkat internasional',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.2.a']:
                                dat = result['V.G.2.a'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.2.a'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.2.a',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.2.a'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.G.2.b' in result and any(result['V.G.2.b']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.2.b'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'b. Tingkat nasional',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.2.b']:
                                dat = result['V.G.2.b'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.2.b'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.2.b',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.2.b'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


                    if 'V.G.2.c' in result and any(result['V.G.2.c']):
                        #======================revisi idris==============================================
                        dumm = []
                        for key,value in result['V.G.2.c'].items():
                            dumm.append(key)
                        semester = sorted(set(dumm), key=getSort)
                        #=================================================================================
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'c. Tingkat provinsi',fmt_box)
                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        current_row5 = current_row5 + 1
                        start_code = current_row5

                        no =  1
                        #=====================revisi==================================
                        for sem in semester:
                            if sem in result['V.G.2.c']:
                                dat = result['V.G.2.c'][sem]
                        #=============================================================
                            #for period,lines in result['V.G.2.c'].items():
                                if len(dat) > 1:
                                    sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                                else:
                                    sheet5.write('J' + str(current_row5),sem,fmt_box)
                                            
                                i = 1
                                for line in dat:
                                    sheet5.set_row(current_row5-1,30)
                                    sheet5.write('C' + str(current_row5),no,fmt_box)
                                    sheet5.merge_range('D' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                    sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                    sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                    sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                    sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                    i += 1
                                    no += 1
                                    current_row5 = current_row5 + 1

                        for x in ['J','K','L','M','N','O']:
                            sheet5.write(x + str(current_row5),'',fmt_box)
                        sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),'Total V.G.2.c',fmt_box)
                        sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                        total['V.G.2.c'] = '=Lamp.5!N' + str(current_row5)
                        current_row5 = current_row5 + 1


            if any(k in result for k in ['V.H.1','V.H.2','V.H.3']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.H')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menulis buku pelajaran SLTA ke bawah yang diterbitkan dan diedarkan secara Nasional',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1

                if 'V.H.1' in result and any(result['V.H.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.H.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'1. Buku SLTA atau setingkat',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.H.1']:
                            dat = result['V.H.1'][sem]
                    #=============================================================
                        #for period,lines in result['V.H.1'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.H.1',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.H.1'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.H.2' in result and any(result['V.H.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.H.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'2. Buku SLTP atau setingkat',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.H.2']:
                            dat = result['V.H.2'][sem]
                    #=============================================================
                        #for period,lines in result['V.H.2'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.H.2',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.H.2'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.H.3' in result and any(result['V.H.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.H.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'3. Buku SD atau setingkat',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.H.3']:
                            dat = result['V.H.3'][sem]
                    #=============================================================
                        #for period,lines in result['V.H.3'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.H.3',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.H.3'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


            if any(k in result for k in ['V.I.1','V.I.2','V.I.3']):
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.I')
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Mempunyai prestasi dibidang olah raga/humaniora',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1

                if 'V.I.1' in result and any(result['V.I.1']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.I.1'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'1. Tingkat Internasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.I.1']:
                            dat = result['V.I.1'][sem]
                    #=============================================================
                        #for period,lines in result['V.I.1'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.I.1',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.I.1'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.I.2' in result and any(result['V.I.2']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.I.2'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'2. Tingkat Nasional',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.I.2']:
                            dat = result['V.I.2'][sem]
                    #=============================================================
                        #for period,lines in result['V.I.2'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.I.2',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.I.2'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


                if 'V.I.3' in result and any(result['V.I.3']):
                    #======================revisi idris==============================================
                    dumm = []
                    for key,value in result['V.I.3'].items():
                        dumm.append(key)
                    semester = sorted(set(dumm), key=getSort)
                    #=================================================================================
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'3. Tingkat Daerah',fmt_box)
                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    current_row5 = current_row5 + 1
                    start_code = current_row5

                    no =  1
                    #=====================revisi==================================
                    for sem in semester:
                        if sem in result['V.I.3']:
                            dat = result['V.I.3'][sem]
                    #=============================================================
                        #for period,lines in result['V.I.3'].items():
                            if len(dat) > 1:
                                sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                            else:
                                sheet5.write('J' + str(current_row5),sem,fmt_box)
                                        
                            i = 1
                            for line in dat:
                                sheet5.set_row(current_row5-1,30)
                                sheet5.write('B' + str(current_row5),no,fmt_box)
                                sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                                sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                                sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                                sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                                sheet5.write('O' + str(current_row5),line.note,fmt_box)
                                i += 1
                                no += 1
                                current_row5 = current_row5 + 1

                    for x in ['J','K','L','M','N','O']:
                        sheet5.write(x + str(current_row5),'',fmt_box)
                    sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.I.3',fmt_box)
                    sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                    total['V.I.3'] = '=Lamp.5!N' + str(current_row5)
                    current_row5 = current_row5 + 1


            if 'V.J' in result and any(result['V.J']):
                #======================revisi idris==============================================
                dumm = []
                for key,value in result['V.J'].items():
                    dumm.append(key)
                semester = sorted(set(dumm), key=getSort)
                #=================================================================================
                sheet5.set_row(current_row5-1,30)
                sheet5.write('A' + str(current_row5),'V.J')               
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Menjadi anggota tim penilai jabatan Akademik Dosen',fmt_box)
                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                current_row5 = current_row5 + 1
                start_code = current_row5

                no =  1
                #=====================revisi==================================
                for sem in semester:
                    if sem in result['V.J']:
                        dat = result['V.J'][sem]
                #=============================================================
                    #for period,lines in result['V.J'].items():
                        if len(dat) > 1:
                            sheet5.merge_range('J' + str(current_row5) + ':J' + str(current_row5 + len(dat) - 1),sem,fmt_box)
                        else:
                            sheet5.write('J' + str(current_row5),sem,fmt_box)
                                    
                        i = 1
                        for line in dat:
                            sheet5.set_row(current_row5-1,30)
                            sheet5.write('B' + str(current_row5),no,fmt_box)
                            sheet5.merge_range('C' + str(current_row5) + ':I' + str(current_row5),line.name,fmt_box)
                            sheet5.write('L' + str(current_row5),line.volume,fmt_box)
                            sheet5.write('M' + str(current_row5),line.score_max,fmt_box)
                            sheet5.write('N' + str(current_row5),'=L' + str(current_row5) +'*M' + str(current_row5),fmt_box)
                            sheet5.write('O' + str(current_row5),line.note,fmt_box)
                            i += 1
                            no += 1
                            current_row5 = current_row5 + 1

                for x in ['J','K','L','M','N','O']:
                    sheet5.write(x + str(current_row5),'',fmt_box)
                sheet5.merge_range('B' + str(current_row5) + ':I' + str(current_row5),'Total V.J',fmt_box)
                sheet5.write('N' + str(current_row5),'=SUM(N' + str(start_code) + ':N' + str(current_row5-1) + ')',fmt_box)
                total['V.J'] = '=Lamp.5!N' + str(current_row5)
                current_row5 = current_row5 + 1


        #=============================revisi====================================================
        djk = {'male':'Laki-laki','Male':'Laki-laki','female':'Perempuan','Female':'Perempuan'}
        cpns_s = dupak.employee_id.cpns_start
        cpns_s = datetime.strptime(dupak.employee_id.cpns_start, '%Y-%m-%d')
        today = datetime.today()
        months = (today.year - cpns_s.year)*12 + today.month - cpns_s.month
        hasil = str(months/12) + ' tahun ' + str(months%12) + ' bulan'
        #=======================================================================================

        #sheet Lamp6
        sheet6.set_column('A:A',1.71)
        sheet6.set_column('B:B',2.57)
        sheet6.set_column('C:C',1.86)
        sheet6.set_column('D:F',5.29)
        sheet6.set_column('G:G',10.29)
        sheet6.set_column('H:I',3.57)
        sheet6.set_column('J:J',8.71)
        sheet6.set_column('K:N',7.29)
        sheet6.set_row(0,6.75)
        sheet6.set_row(1,103.5)
        sheet6.write('J2','Lampiran VI:',fmt_wrap)
        sheet6.merge_range('K2:N2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet6.merge_range('A4:N4','DAFTAR USUL PENETAPAN ANGKA KREDIT',fmt_headercenter)
        sheet6.merge_range('A5:N5','JABATAN FUNGSIONAL DOSEN',fmt_headercenter)
        start = datetime.strptime(dupak.start, '%Y-%m-%d').strftime('%d %B %Y')
        finish = datetime.strptime(dupak.finish, '%Y-%m-%d').strftime('%d %B %Y') 
        sheet6.merge_range('A9:M9','Masa Penilaian Tanggal   '+ start +'   s/d Tanggal  '+ finish,fmt_center)
        sheet6.set_row(9,7.5)
        sheet6.merge_range('A11:A22','I',fmt_box)
        sheet6.write('B11','No.',fmt_box)
        sheet6.merge_range('C11:N11','KETERANGAN PERORANGAN',fmt_box)
        sheet6.write('B12','1.',fmt_box)
        sheet6.merge_range('C12:G12','Nama',fmt_box)
        sheet6.merge_range('H12:N12',dupak.employee_id.name,fmt_box)
        sheet6.write('B13','2.',fmt_box)
        sheet6.merge_range('C13:G13','NIP',fmt_box)
        sheet6.merge_range('H13:N13',dupak.employee_id.nip_new,fmt_box)
        sheet6.write('B14','3.',fmt_box)
        sheet6.merge_range('C14:G14','Nomor Seri Karpeg',fmt_box)
        sheet6.merge_range('H14:N14',dupak.employee_id.employee_card,fmt_box)
        sheet6.write('B15','4.',fmt_box)
        sheet6.merge_range('C15:G15','Pangkat dan Golongan Ruang/ TMT',fmt_box)
        sheet6.merge_range('H15:N15',dupak.pangkat,fmt_box)
        sheet6.write('B16','5.',fmt_box)
        sheet6.merge_range('C16:G16','Tempat dan Tanggal Lahir',fmt_box)
        sheet6.merge_range('H16:N16',dupak.employee_id.birthplace + ', ' + datetime.strptime(dupak.employee_id.birthday, '%Y-%m-%d').strftime('%d %B %Y'),fmt_box)
        sheet6.write('B17','6.',fmt_box)
        sheet6.merge_range('C17:G17','Jenis Kelamin',fmt_box)
        sheet6.merge_range('H17:N17',dupak.employee_id.gender,fmt_box)
        sheet6.write('B18','7.',fmt_box)
        sheet6.merge_range('C18:G18','Pendidikan Tertinggi',fmt_box)
        sheet6.merge_range('H18:N18',dupak.education,fmt_box)
        sheet6.write('B19','8.',fmt_box)
        sheet6.merge_range('C19:G19','Jabatan Akademik Dosen / TMT',fmt_box)
        sheet6.merge_range('H19:N19',dupak.jabatan,fmt_box)
        sheet6.merge_range('B20:B21','9.',fmt_box)
        sheet6.merge_range('C20:F21','Masa Kerja Golongan',fmt_box)
        sheet6.write('G20','Lama',fmt_box)
        sheet6.merge_range('H20:N20',hasil,fmt_box)
        sheet6.write('G21','Baru',fmt_box)
        sheet6.merge_range('H21:N21','',fmt_box)
        sheet6.write('B22','10.')
        sheet6.merge_range('C22:G22','Unit Kerja',fmt_box)
        sheet6.merge_range('H22:N22',conf_school,fmt_box)
        sheet6.merge_range('A23:A33','II',fmt_box)
        sheet6.merge_range('B23:K23','PENETAPAN ANGKA KREDIT',fmt_box)
        sheet6.write('L23','LAMA',fmt_box)
        sheet6.write('M23','BARU',fmt_box)
        sheet6.write('N23','JUMLAH',fmt_box)
        sheet6.merge_range('B24:B29',1,fmt_box)
        sheet6.merge_range('C24:K24','UNSUR UTAMA',fmt_box)
        for x in ['L','M','N']:
            sheet6.write(x + str(24),'',fmt_box)
        sheet6.write('C25','A',fmt_box)
        sheet6.merge_range('D25:K25','Pendidikan',fmt_box)
        sheet6.write('C26','B',fmt_box)
        sheet6.merge_range('D26:K26','Melaksanakan Pendidikan',fmt_box)
        sheet6.write('C27','C',fmt_box)
        sheet6.merge_range('D27:K27','Melaksanakan Penelitian',fmt_box)
        sheet6.write('C28','D',fmt_box)
        sheet6.merge_range('D28:K28','Melaksanakan Pengabdian kepada Masyarakat',fmt_box)
        sheet6.merge_range('C29:K29','Jumlah Unsur Utama',fmt_box)
        sheet6.merge_range('B30:B32',2,fmt_box)
        sheet6.merge_range('C30:K30','UNSUR PENUNJANG',fmt_box)
        for x in ['L','M','N']:
            sheet6.write(x + str(30),'',fmt_box)
        sheet6.merge_range('C31:K31','Penunjang Tugas Dosen',fmt_box)
        sheet6.merge_range('C32:K32','Jumlah Unsur Penunjang',fmt_box)
        sheet6.merge_range('B33:K33','Jumlah Unsur Utama dan Unsur Penunjang',fmt_box)
        sheet6.write('L25',dupak.last_id.education_score,fmt_box)
        sheet6.write('L26',dupak.last_id.pendidikan_score,fmt_box)
        sheet6.write('L27',dupak.last_id.penelitian_score,fmt_box)
        sheet6.write('L28',dupak.last_id.pengabdian_score,fmt_box)
        sheet6.write('L31',dupak.last_id.penunjang_score,fmt_box)
        sheet6.write('M25',dupak.education_score,fmt_box)
        sheet6.write('M26',dupak.pendidikan_score,fmt_box)
        sheet6.write('M27',dupak.penelitian_score,fmt_box)
        sheet6.write('M28',dupak.pengabdian_score,fmt_box)
        sheet6.write('M31',dupak.penunjang_score,fmt_box)
        sheet6.write('N25','=L25+M25',fmt_box)
        sheet6.write('N26','=L26+M26',fmt_box)
        sheet6.write('N27','=L27+M27',fmt_box)
        sheet6.write('N28','=L28+M28',fmt_box)
        sheet6.write('N31','=L31+M31',fmt_box)
        sheet6.write('L29','=SUM(L25:L28)',fmt_box)
        sheet6.write('M29','=SUM(M25:M28)',fmt_box)
        sheet6.write('N29','=SUM(N25:N28)',fmt_box)
        sheet6.write('L32','=SUM(L31:L31)',fmt_box)
        sheet6.write('M32','=SUM(M31:M31)',fmt_box)
        sheet6.write('N32','=SUM(N31:N31)',fmt_box)
        sheet6.write('L33','=L29+L32',fmt_box)
        sheet6.write('M33','=M29+M32',fmt_box)
        sheet6.write('N33','=N29+N32',fmt_box)
        sheet6.write('A34','III',fmt_box)
        sheet6.merge_range('B34:N34','Dapat dipertimbangkan untuk dinaikkan jabatannya menjadi ' + dupak.next_jabatan + ' dan pangkat menjadi ' + dupak.next_pangkat + ' terhitung mulai tanggal ...',fmt_box)

        #sheet Lamp1
        sheet1.set_column('A:A',2.86)
        sheet1.set_column('B:C',1.29)
        sheet1.set_column('D:D',1.71)
        sheet1.set_column('E:E',1.57)
        sheet1.set_column('F:F',16.43)
        sheet1.set_column('G:G',5.57)
        sheet1.set_column('H:H',10.14)
        sheet1.set_column('I:I',5.43)
        sheet1.set_column('J:J',8.29)
        sheet1.set_column('K:K',7)
        sheet1.set_column('L:L',5.43)
        sheet1.set_column('M:M',5)
        sheet1.set_column('N:N',7)
        sheet1.set_row(0,6.75)
        sheet1.set_row(1,103.5)
        sheet1.write('J2','Lampiran I:',fmt_wrap)
        sheet1.merge_range('K2:N2','Peraturan Bersama Menteri Pendidikan dan Kebudayaan dan Kepala Badan Kepegawaian Negara\nNomor : 4/VIII/PB/2014\nNomor : 24 Tahun 2014\nTanggal 12 Agustus 2014',fmt_wrap)
        sheet1.merge_range('A4:N4','DAFTAR USUL PENETAPAN ANGKA KREDIT',fmt_headercenter)
        sheet1.merge_range('A5:N5','JABATAN FUNGSIONAL DOSEN',fmt_headercenter)
        start = datetime.strptime(dupak.start, '%Y-%m-%d').strftime('%d %B %Y')
        finish = datetime.strptime(dupak.finish, '%Y-%m-%d').strftime('%d %B %Y') 
        sheet1.merge_range('A9:M9','Masa Penilaian Tanggal   '+ start +'   s/d Tanggal  '+ finish,fmt_center)
        sheet1.set_row(9,7.5)
        sheet1.write('A11','No.',fmt_box)
        sheet1.merge_range('B11:N11','KETERANGAN PERORANGAN',fmt_centerbox)
        sheet1.write('A12','1.',fmt_box)
        sheet1.merge_range('B12:G12','Nama',fmt_box)
        sheet1.merge_range('H12:N12',dupak.employee_id.name,fmt_box)
        sheet1.write('A13','2.',fmt_box)
        sheet1.merge_range('B13:G13','NIP',fmt_box)
        sheet1.merge_range('H13:N13',dupak.employee_id.nip_new,fmt_box)
        sheet1.write('A14','3.',fmt_box)
        sheet1.merge_range('B14:G14','Nomor Seri Karpeg',fmt_box)
        sheet1.merge_range('H14:N14',dupak.employee_id.employee_card,fmt_box)
        sheet1.write('A15','4.',fmt_box)
        sheet1.merge_range('B15:G15','Pangkat dan Golongan Ruang/ TMT',fmt_box)
        sheet1.merge_range('H15:N15',dupak.pangkat,fmt_box)
        sheet1.write('A16','5.',fmt_box)
        sheet1.merge_range('B16:G16','Tempat dan Tanggal Lahir',fmt_box)
        sheet1.merge_range('H16:N16',dupak.employee_id.birthplace + ', ' + datetime.strptime(dupak.employee_id.birthday, '%Y-%m-%d').strftime('%d %B %Y'),fmt_box)
        sheet1.write('A17','6.',fmt_box)
        sheet1.merge_range('B17:G17','Jenis Kelamin',fmt_box)
        #================revisi============================================
        sheet1.merge_range('H17:N17',djk[dupak.employee_id.gender],fmt_box)
        #==================================================================
        sheet1.write('A18','7.',fmt_box)
        sheet1.merge_range('B18:G18','Pendidikan Tertinggi',fmt_box)
        sheet1.merge_range('H18:N18',dupak.education,fmt_box)
        sheet1.write('A19','8.',fmt_box)
        sheet1.merge_range('B19:G19','Jabatan Akademik Dosen / TMT',fmt_box)
        sheet1.merge_range('H19:N19',dupak.jabatan,fmt_box)
        sheet1.merge_range('A20:A21','9.',fmt_box)
        sheet1.merge_range('B20:F21','Masa Kerja Golongan',fmt_box)
        sheet1.write('G20','Lama',fmt_box)
        #=============================revisi========================dupak.last_period
        sheet1.merge_range('H20:N20',hasil,fmt_box)
        sheet1.write('G21','Baru',fmt_box)
        sheet1.merge_range('H21:N21','',fmt_box)
        #=========================================================dupak.period
        sheet1.write('A22','10.',fmt_box)
        sheet1.merge_range('B22:G22','Unit Kerja',fmt_box)
        sheet1.merge_range('H22:N22',conf_school,fmt_box)
        sheet1.merge_range('A24:A27','NO',fmt_centerbox)
        sheet1.merge_range('B24:N24','UNSUR YANG DINILAI',fmt_centerbox)
        sheet1.merge_range('B25:H27','UNSUR, SUB UNSUR DAN BUTIR KEGIATAN',fmt_centerbox)
        sheet1.merge_range('I25:N25','ANGKA KREDIT MENURUT',fmt_centerbox)
        sheet1.merge_range('I26:K26','INSTANSI PENGUSUL',fmt_centerbox)
        sheet1.merge_range('L26:N26','TIM PENILAI',fmt_centerbox)
        sheet1.write('I27','LAMA',fmt_centerbox)
        sheet1.write('J27','BARU',fmt_centerbox)
        sheet1.write('K27','JUMLAH',fmt_centerbox)
        sheet1.write('L27','LAMA',fmt_centerbox)
        sheet1.write('M27','BARU',fmt_centerbox)
        sheet1.write('N27','JUMLAH',fmt_centerbox)
        sheet1.write('A28',1,fmt_centerbox)
        sheet1.merge_range('B28:H28',2,fmt_centerbox)
        sheet1.write('I28',3,fmt_centerbox)
        sheet1.write('J28',4,fmt_centerbox)
        sheet1.write('K28',5,fmt_centerbox)
        sheet1.write('L28',6,fmt_centerbox)
        sheet1.write('M28',7,fmt_centerbox)
        sheet1.write('N28',8,fmt_centerbox)
        sheet1.merge_range('A29:A35','I',fmt_box)
        sheet1.merge_range('B29:H29','PENDIDIKAN',fmt_box)
        sheet1.merge_range('B30:B32','A',fmt_box)
        sheet1.merge_range('C30:H30','Pendidikan Formal',fmt_box)
        sheet1.write('C31',1,fmt_box)
        sheet1.merge_range('D31:H31','Doktor (S3)',fmt_box)
        sheet1.write('C32',2,fmt_box)
        sheet1.merge_range('D32:H32','Magister (S2)',fmt_box)
        sheet1.merge_range('B33:B34','B',fmt_box)
        sheet1.merge_range('C33:H33','Pendidikan dan Pelatihan Prajabatan',fmt_box)
        sheet1.merge_range('D34:H34','Pendidikan dan Pelatihan Prajabatan Golongan III',fmt_box)
        sheet1.merge_range('B35:H35','Jumlah Pendidikan',fmt_box)
        sheet1.merge_range('A36:A83','II',fmt_box)
        sheet1.merge_range('B36:H36','PELAKSANAAN PENDIDIKAN',fmt_box)
        sheet1.write('B37','A',fmt_box)
        sheet1.merge_range('C37:H37','Melaksanakan perkuliahan/tutorial & membimbing,menguji serta menyelenggarakan pendidikan di laboratorium, praktek keguruan, bengkel/studio/kebun percobaan/teknologi pengajaran & praktek lapangan',fmt_box)
        sheet1.write('B38','B',fmt_box)
        sheet1.merge_range('C38:H38','Membimbing seminar mahasiswa',fmt_box)
        sheet1.write('B39','C',fmt_box)
        sheet1.merge_range('C39:H39','Membimbing Kuliah Kerja Nyata (KKN), Praktek Kerja Nyata (PKN), Praktek Kerja Lapangan (PKL)',fmt_box)
        sheet1.merge_range('B40:B50','D',fmt_box)
        sheet1.merge_range('C40:H40','Membimbing dan ikut membimbing dalam menghasilkan laporan akhir studi/skripsi/thesis/disertasi',fmt_box)
        sheet1.merge_range('C41:C45',1,fmt_box)
        sheet1.merge_range('D41:H41','Pembimbing Utama',fmt_box)
        sheet1.write('D42','a.',fmt_box)
        sheet1.merge_range('E42:H42','Disertasi',fmt_box)
        sheet1.write('D43','b.',fmt_box)
        sheet1.merge_range('E43:H43','Thesis',fmt_box)
        sheet1.write('D44','c.',fmt_box)
        sheet1.merge_range('E44:H44','Skripsi',fmt_box)
        sheet1.write('D45','d.',fmt_box)
        sheet1.merge_range('E45:H45','Laporan akhir',fmt_box)
        sheet1.merge_range('C46:C50',2,fmt_box)
        sheet1.merge_range('D46:H46','Pembimbing pendamping/pembantu',fmt_box)
        sheet1.write('D47','a.',fmt_box)
        sheet1.merge_range('E47:H47','Disertasi',fmt_box)
        sheet1.write('D48','b.',fmt_box)
        sheet1.merge_range('E48:H48','Thesis',fmt_box)
        sheet1.write('D49','c.',fmt_box)
        sheet1.merge_range('E49:H49','Skripsi',fmt_box)
        sheet1.write('D50','d.',fmt_box)
        sheet1.merge_range('E50:H50','Laporan akhir',fmt_box)
        sheet1.merge_range('B51:B53','E',fmt_box)
        sheet1.merge_range('C51:H51','Bertugas sebagai penguji pada Ujian Akhir',fmt_box)
        sheet1.write('C52',1,fmt_box)
        sheet1.merge_range('D52:H52','Ketua penguji',fmt_box)
        sheet1.write('C53',2,fmt_box)
        sheet1.merge_range('D53:H53','Anggota penguji',fmt_box)
        sheet1.write('B54','F',fmt_box)
        sheet1.merge_range('C54:H54','Membina kegiatan mahasiswa dibidang akademik dan kemahasiswaan',fmt_box)
        sheet1.write('B55','G',fmt_box)
        sheet1.merge_range('C55:H55','Mengembangkan program kuliah',fmt_box)
        sheet1.merge_range('B56:B58','H',fmt_box)
        sheet1.merge_range('C56:H56','Mengembangkan bahan pengajaran',fmt_box)
        sheet1.write('C57',1,fmt_box)
        sheet1.merge_range('D57:H57','Buku Ajar',fmt_box)
        sheet1.write('C58',2,fmt_box)
        sheet1.merge_range('D58:H58','Diktat, Modul, Petunjuk Praktikum, Model, Alat Bantu, audio visual, naskah tutorial',fmt_box)
        sheet1.write('B59','I',fmt_box)
        sheet1.merge_range('C59:H59','Melakukan kegiatan orasi ilmiah pada perguruan tinggi',fmt_box)
        sheet1.merge_range('B60:B68','J',fmt_box)
        sheet1.merge_range('C60:H60','Menduduki jabatan pimpinan perguruan tinggi',fmt_box)
        sheet1.write('C61',1,fmt_box)
        sheet1.merge_range('D61:H61','Rektor',fmt_box)
        sheet1.write('C62',2,fmt_box)
        sheet1.merge_range('D62:H62','Pembantu Rektor/Dekan/Direktur PPs',fmt_box)
        sheet1.write('C63',3,fmt_box)
        sheet1.merge_range('D63:H63','Ketua Sekolah Tinggi/Pembantu Dekan/ Asisten Dir. Program Pasca Sarjana/ Dir. Politeknik',fmt_box)
        sheet1.write('C64',4,fmt_box)
        sheet1.merge_range('D64:H64','Pembantu Ketua Sekolah Tinggi/Pembantu Direktur Politeknik',fmt_box)
        sheet1.write('C65',5,fmt_box)
        sheet1.merge_range('D65:H65','Direktur Akademik',fmt_box)
        sheet1.write('C66',6,fmt_box)
        sheet1.merge_range('D66:H66','Pembantu Dir. Akademi/Ketua Jurusan/ Bagian pada Univ/Inst/Sekolah Tinggi',fmt_box)
        sheet1.write('C67',7,fmt_box)
        sheet1.merge_range('D67:H67','Ketua Jurusan pada Politeknik/Akademi/ Sekretaris Jurusan/Bagian pada Univ/Inst/ST.',fmt_box)
        sheet1.write('C68',8,fmt_box)
        sheet1.merge_range('D68:H68','Sekretaris Jurusan pada Politeknik/Akademi dan Kepala Laboratorium Universitas/Institut/Sekolah Tinggi/Politeknik/Akademik',fmt_box)
        sheet1.merge_range('B69:B71','K',fmt_box)
        sheet1.merge_range('C69:H69','Membimbing Akademik dosen yang lebih rendah jabatan fungsionalnya',fmt_box)
        sheet1.write('C70',1,fmt_box)
        sheet1.merge_range('D70:H70','Pembimbing pencangkokan',fmt_box)
        sheet1.write('C71',2,fmt_box)
        sheet1.merge_range('D71:H71','Reguler',fmt_box)
        sheet1.merge_range('B72:B74','L',fmt_box)
        sheet1.merge_range('C72:H72','Melaksanakan kegiatan datasering dan pencangkokan dosen',fmt_box)
        sheet1.write('C73',1,fmt_box)
        sheet1.merge_range('D73:H73','Detasering',fmt_box)
        sheet1.write('C74',2,fmt_box)
        sheet1.merge_range('D74:H74','Pencangkokan',fmt_box)
        sheet1.merge_range('B75:B82','M',fmt_box)
        sheet1.merge_range('C75:H75','Melakukan kegiatan pengembangan diri untuk meningkatkan kompetensi',fmt_box)
        sheet1.write('C76',1,fmt_box)
        sheet1.merge_range('D76:H76','Lamanya lebih dari 960 jam',fmt_box)
        sheet1.write('C77',2,fmt_box)
        sheet1.merge_range('D77:H77','Lamanya antara 641-960 jam',fmt_box)
        sheet1.write('C78',3,fmt_box)
        sheet1.merge_range('D78:H78','Lamanya antara 481-640 jam',fmt_box)
        sheet1.write('C79',4,fmt_box)
        sheet1.merge_range('D79:H79','Lamanya antara 161-480 jam',fmt_box)
        sheet1.write('C80',5,fmt_box)
        sheet1.merge_range('D80:H80','Lamanya antara 81-160 jam',fmt_box)
        sheet1.write('C81',6,fmt_box)
        sheet1.merge_range('D81:H81','Lamanya antara 31-80 jam',fmt_box)
        sheet1.write('C82',7,fmt_box)
        sheet1.merge_range('D82:H82','Lamanya antara 10-30 jam',fmt_box)
        sheet1.merge_range('B83:H83','Jumlah Pelaksanaan Pendidikan',fmt_box)
        sheet1.merge_range('A84:A112','III',fmt_box)
        sheet1.merge_range('B84:H84','PELAKSANAAN PENELITIAN',fmt_box)
        sheet1.merge_range('B85:B100','A',fmt_box)
        sheet1.merge_range('C85:H85','Menghasilkan Karya Ilmiah',fmt_box)
        sheet1.merge_range('C86:C99',1,fmt_box)
        sheet1.merge_range('D86:H86','Hasil Penelitian atau Pemikiran yang dipublikasikan',fmt_box)
        sheet1.merge_range('D87:D89','a.',fmt_box)
        sheet1.merge_range('E87:H87','Dalam Bentuk',fmt_box)
        sheet1.write('E88',1,fmt_box)
        sheet1.merge_range('F88:H88','Monograf',fmt_box)
        sheet1.write('E89',2,fmt_box)
        sheet1.merge_range('F89:H89','Buku Referensi',fmt_box)
        sheet1.merge_range('D90:D93','b.',fmt_box)
        sheet1.merge_range('E90:H90','Jurnal Ilmiah',fmt_box)
        sheet1.write('E91',1,fmt_box)
        sheet1.merge_range('F91:H91','Internasional',fmt_box)
        sheet1.write('E92',2,fmt_box)
        sheet1.merge_range('F92:H92','Nasional Terakreditasi',fmt_box)
        sheet1.write('E93',3,fmt_box)
        sheet1.merge_range('F93:H93','Nasional tidak Terakreditasi',fmt_box)
        sheet1.merge_range('D94:D98','c.',fmt_box)
        sheet1.merge_range('E94:H94','Seminar',fmt_box)
        sheet1.write('E95',1,fmt_box)
        sheet1.merge_range('F95:H95','Disajikan tingkat Internasional',fmt_box)
        sheet1.write('E96',2,fmt_box)
        sheet1.merge_range('F96:H96','Disajikan tingkat Nasional',fmt_box)
        sheet1.write('E97',3,fmt_box)
        sheet1.merge_range('F97:H97','Poster tingkat Internasional',fmt_box)
        sheet1.write('E98',4,fmt_box)
        sheet1.merge_range('F98:H98','Poster tingkat Nasional',fmt_box)
        sheet1.write('D99','d.',fmt_box)
        sheet1.merge_range('E99:H99','Dalam koran/majalah populer/umum',fmt_box)
        sheet1.write('C100',2,fmt_box)
        sheet1.merge_range('D100:H100','Hasil Penelitian atau Pemikiran yang tidak dipublikasikan (tersimpan di perpustakaan perguruan tinggi)',fmt_box)
        sheet1.merge_range('B101:B102','B',fmt_box)
        sheet1.merge_range('C101:H101','Menerjemahkan/menyadur buku ilmiah',fmt_box)
        sheet1.merge_range('D102:H102','Diterbitkan dan diedarkan secara Nasional',fmt_box)
        sheet1.merge_range('B103:B104','C',fmt_box)
        sheet1.merge_range('C103:H103','Mengedit/menyunting karya ilmiah',fmt_box)
        sheet1.merge_range('D104:H104','Diterbitkan dan diedarkan secara Nasional',fmt_box)
        sheet1.merge_range('B105:B107','D',fmt_box)
        sheet1.merge_range('C105:H105','Membuat rancangan dan karya teknologi yang dipatenkan',fmt_box)
        sheet1.write('C106',1,fmt_box)
        sheet1.merge_range('D106:H106','Internasional',fmt_box)
        sheet1.write('C107',2,fmt_box)
        sheet1.merge_range('D107:H107','Nasional',fmt_box)
        sheet1.merge_range('B108:B111','E',fmt_box)
        sheet1.merge_range('C108:H108','Membuat rancangan & karya teknologi,rancangan & karya seni monumental/seni pertunjukan/karya sastra',fmt_box)
        sheet1.write('C109',1,fmt_box)
        sheet1.merge_range('D109:H109','Tingkat Internasional',fmt_box)
        sheet1.write('C110',2,fmt_box)
        sheet1.merge_range('D110:H110','Tingkat Nasional',fmt_box)
        sheet1.write('C111',3,fmt_box)
        sheet1.merge_range('D111:H111','Tingkat Lokal',fmt_box)
        sheet1.merge_range('B112:H112','Jumlah Penelitian',fmt_box)
        sheet1.merge_range('A113:A135','IV',fmt_box)
        sheet1.merge_range('B113:H113','PELAKSANAAN PENGABDIAN KEPADA MASYARAKAT',fmt_box)
        sheet1.merge_range('B114:B115','A',fmt_box)
        sheet1.merge_range('C114:H114','Menduduki jabatan pimpinan',fmt_box)
        sheet1.merge_range('D115:H115','Menduduki jabatan pimpinan pada lembaga pemerintah/pejabat negara yang harus dibebaskan dari jabatan organiknya',fmt_box)        
        sheet1.merge_range('B116:B117','B',fmt_box)
        sheet1.merge_range('C116:H116','Melaksanakan pengembangan hasil pendidikan dan penelitian',fmt_box)
        sheet1.merge_range('D117:H117','Melaksanakan pengembangan hasil pendidikan & penelitian yg dapat dimanfaatkan oleh masyarakat',fmt_box)        
        sheet1.merge_range('B118:B128','C',fmt_box)
        sheet1.merge_range('C118:H118','Memberi latihan/penyuluhan/penataran/ceramah pada masyarakat',fmt_box)
        sheet1.merge_range('C119:C127',1,fmt_box)
        sheet1.merge_range('D119:H119','Terjadwal/terprogram',fmt_box)
        sheet1.merge_range('D120:D123','a.',fmt_box)
        sheet1.merge_range('E120:H120','Dalam satu semester atau lebih',fmt_box)
        sheet1.write('E121',1,fmt_box)
        sheet1.merge_range('F121:H121','Tingkat Internasional',fmt_box)
        sheet1.write('E122',2,fmt_box)
        sheet1.merge_range('F122:H122','Tingkat Nasional',fmt_box)
        sheet1.write('E123',3,fmt_box)
        sheet1.merge_range('F123:H123','Tingkat Lokal',fmt_box)
        sheet1.merge_range('D124:D127','b.',fmt_box)
        sheet1.merge_range('E124:H124','Dalam satu semester atau lebih',fmt_box)
        sheet1.write('E125',1,fmt_box)
        sheet1.merge_range('F125:H125','Tingkat Internasional',fmt_box)
        sheet1.write('E126',2,fmt_box)
        sheet1.merge_range('F126:H126','Tingkat Nasional',fmt_box)
        sheet1.write('E127',3,fmt_box)
        sheet1.merge_range('F127:H127','Tingkat Lokal',fmt_box)
        sheet1.write('C128',2,fmt_box)
        sheet1.merge_range('D128:H128','Insidental',fmt_box)
        sheet1.merge_range('B129:B132','D',fmt_box)
        sheet1.merge_range('C129:H129','Memberi pelayanan kepada masyarakat atau kegiatan lain yang menunjang pelaksanaan tugas umum pemerintahan dan pembangunan',fmt_box)
        sheet1.write('C130',1,fmt_box)
        sheet1.merge_range('D130:H130','Berdasarkan bidang keahlian',fmt_box)
        sheet1.write('C131',2,fmt_box)
        sheet1.merge_range('D131:H131','Berdasarkan penugasan lembaga perguruan tinggi',fmt_box)
        sheet1.write('C132',3,fmt_box)
        sheet1.merge_range('D132:H132','Berdasarkan fungsi/jabatan',fmt_box)
        sheet1.merge_range('B133:B134','E',fmt_box)
        sheet1.merge_range('C133:H133','Membuat/menulis karya pengabdian',fmt_box)
        sheet1.merge_range('D134:H134','Membuat/menulis karya pengabdian pada masyarakat yang tidak dipublikasikan',fmt_box)
        sheet1.merge_range('B135:H135','Jumlah Pengabdian pada Masyarakat',fmt_box)
        sheet1.merge_range('A136:A187','V',fmt_box)
        sheet1.merge_range('B136:H136','PENUNJANG TUGAS DOSEN',fmt_box)
        sheet1.merge_range('B137:B139','A',fmt_box)
        sheet1.merge_range('C137:H137','Menjadi anggota dalam suatu Panitia/Badan pada Perguruan Tinggi',fmt_box)
        sheet1.write('C138',1,fmt_box)
        sheet1.merge_range('D138:H138','Sebagai ketua/wakil ketua merangkap anggota',fmt_box)
        sheet1.write('C139',2,fmt_box)
        sheet1.merge_range('D139:H139','Sebagai anggota',fmt_box)
        sheet1.merge_range('B140:B146','B',fmt_box)
        sheet1.merge_range('C140:H140','Menjadi anggota paniti/badan pada lembaga pemerintah',fmt_box)
        sheet1.merge_range('C141:C143',1,fmt_box)
        sheet1.merge_range('D141:H141','Panitia Pusat',fmt_box)
        sheet1.write('D142','a',fmt_box)
        sheet1.merge_range('E142:H142','Ketua/wakil ketua',fmt_box)
        sheet1.write('D143','b',fmt_box)
        sheet1.merge_range('E143:H143','Anggota',fmt_box)
        sheet1.merge_range('C144:C146',2,fmt_box)
        sheet1.merge_range('D144:H144','Panitia daerah',fmt_box)
        sheet1.write('D145','a',fmt_box)
        sheet1.merge_range('E145:H145','Ketua/wakil ketua',fmt_box)
        sheet1.write('D146','b',fmt_box)
        sheet1.merge_range('E146:H146','Anggota',fmt_box)
        sheet1.merge_range('B147:B155','C',fmt_box)
        sheet1.merge_range('C147:H147','Menjadi anggota organisasi Profesi',fmt_box)
        sheet1.merge_range('C148:C151',1,fmt_box)
        sheet1.merge_range('D148:H148','Tingkat Internasional',fmt_box)
        sheet1.write('D149','a',fmt_box)
        sheet1.merge_range('E149:H149','Pengurus',fmt_box)
        sheet1.write('D150','b',fmt_box)
        sheet1.merge_range('E150:H150','Anggota atas permintaan',fmt_box)
        sheet1.write('D151','c',fmt_box)
        sheet1.merge_range('E151:H151','Anggota',fmt_box)
        sheet1.merge_range('C152:C155',2,fmt_box)
        sheet1.merge_range('D152:H152','Tingkat Nasional',fmt_box)
        sheet1.write('D153','a',fmt_box)
        sheet1.merge_range('E153:H153','Pengurus',fmt_box)
        sheet1.write('D154','b',fmt_box)
        sheet1.merge_range('E154:H154','Anggota atas permintaan',fmt_box)
        sheet1.write('D155','c',fmt_box)
        sheet1.merge_range('E155:H155','Anggota',fmt_box)
        sheet1.merge_range('B156:B157','D',fmt_box)
        sheet1.merge_range('C156:H156','Mewakili Perguruan Tinggi/Lembaga Pemerintah',fmt_box)
        sheet1.merge_range('D157:H157','Mewakili Perguruan Tinggi/Lembaga pemerintah duduk dalam panitia antar Lembaga',fmt_box)
        sheet1.merge_range('B158:B160','E',fmt_box)
        sheet1.merge_range('C158:H158','Menjadi anggota delegasi Nasional ke pertemuan Internasional',fmt_box)
        sheet1.write('C159',1,fmt_box)
        sheet1.merge_range('D159:H159','Sebagai ketua delegasi',fmt_box)
        sheet1.write('C160',2,fmt_box)
        sheet1.merge_range('D160:H160','Sebagai anggota delegasi',fmt_box)
        sheet1.merge_range('B161:B167','F',fmt_box)
        sheet1.merge_range('C161:H161','Berperan serta aktif dalam pertemuan ilmiah',fmt_box)
        sheet1.merge_range('C162:C164',1,fmt_box)
        sheet1.merge_range('D162:H162','Tiingkat internasional/nasional/regional sebagai:',fmt_box)
        sheet1.write('D163','a',fmt_box)
        sheet1.merge_range('E163:H163','Ketua',fmt_box)
        sheet1.write('D164','b',fmt_box)
        sheet1.merge_range('E164:H164','Anggota',fmt_box)
        sheet1.merge_range('C165:C167',2,fmt_box)
        sheet1.merge_range('D165:H165','Di lingkungan perguruan tinggi sendiri sebagai',fmt_box)
        sheet1.write('D166','a',fmt_box)
        sheet1.merge_range('E166:H166','Ketua',fmt_box)
        sheet1.write('D167','b',fmt_box)
        sheet1.merge_range('E167:H167','Anggota',fmt_box)
        sheet1.merge_range('B168:B176','G',fmt_box)
        sheet1.merge_range('C168:H168','Mendapat penghargaan/tanda jasa',fmt_box)
        sheet1.merge_range('C169:C172',1,fmt_box)
        sheet1.merge_range('D169:H169','Penghargaan/tanda jasa Satyalancana Karya Satya',fmt_box)
        sheet1.write('D170','a',fmt_box)
        sheet1.merge_range('E170:H170','30 (tiga puluh) tahun',fmt_box)
        sheet1.write('D171','b',fmt_box)
        sheet1.merge_range('E171:H171','20 (dua puluh) tahun',fmt_box)
        sheet1.write('D172','c',fmt_box)
        sheet1.merge_range('E172:H172','10 (sepuluh) tahun',fmt_box)
        sheet1.merge_range('C173:C176',2,fmt_box)
        sheet1.merge_range('D173:H173','Memperoleh penghargaan lainnya',fmt_box)
        sheet1.write('D174','a',fmt_box)
        sheet1.merge_range('E174:H174','Tingkat internasional',fmt_box)
        sheet1.write('D175','b',fmt_box)
        sheet1.merge_range('E175:H175','Tingkat nasional',fmt_box)
        sheet1.write('D176','c',fmt_box)
        sheet1.merge_range('E176:H176','Tingkat provinsi',fmt_box)
        sheet1.merge_range('B177:B180','H',fmt_box)
        sheet1.merge_range('C177:H177','Menulis buku pelajaran SLTA ke bawah yang diterbitkan dan diedarkan secara Nasional',fmt_box)
        sheet1.write('C178',1,fmt_box)
        sheet1.merge_range('D178:H178','Buku SLTA atau setingkat',fmt_box)
        sheet1.write('C179',2,fmt_box)
        sheet1.merge_range('D179:H179','Buku SLTP atau setingkat',fmt_box)
        sheet1.write('C180',3,fmt_box)
        sheet1.merge_range('D180:H180','Buku SD atau setingkat',fmt_box)
        sheet1.merge_range('B181:B184','I',fmt_box)
        sheet1.merge_range('C181:H181','Mempunyai prestasi di bidang olah raga/humaniora',fmt_box)
        sheet1.write('C182',1,fmt_box)
        sheet1.merge_range('D182:H182','Tingkat Internasional',fmt_box)
        sheet1.write('C183',2,fmt_box)
        sheet1.merge_range('D183:H183','Tingkat Nasional',fmt_box)
        sheet1.write('C184',3,fmt_box)
        sheet1.merge_range('D184:H184','Tingkat daerah/lokal',fmt_box)
        sheet1.merge_range('B185:B186','J',fmt_box)
        sheet1.merge_range('C185:H185','Keanggotaan dalam tim penilai',fmt_box)
        sheet1.merge_range('D186:H186','Menjadi anggota tim penilaian jabatan Akademik Dosen',fmt_box)
        sheet1.merge_range('B187:H187','Jumlah Penunjang',fmt_box)
        sheet1.merge_range('A188:H188','Jumlah Unsur Utama dan Unsur Penunjang',fmt_box)
        sheet1.write('A190','III.')
        sheet1.merge_range('B190:H190','LAMPIRAN PENDUKUNG DUPAK')
        sheet1.write('B191','1.')
        sheet1.write('C191','Surat pernyataan telah melaksanakan kegiatan pendidikan')
        sheet1.write('B192','2.')
        sheet1.write('C192','Surat pernyataan telah melakukan kegiatan pengajaran')
        sheet1.write('B193','3.')
        sheet1.write('C193','Surat pernyataan telah melaksanakan kegiatan pengabdian kepada masyarakat')
        sheet1.write('B194','4.')
        sheet1.write('C194','Surat pernyataan telah melakukan kegiatan penunjang')
        sheet1.write('A195','IV.')
        sheet1.merge_range('B196:H209','')
        sheet1.merge_range('B195:H195','Catatan Pejabat Pengusul:')
        sheet1.write('I201','Bandung')
        sheet1.write('I202',conf_school)
        sheet1.write('I203','Wakil Dekan Bidang Sumberdaya')
        sheet1.write('I207',conf_wds_name)
        sheet1.write('I208',conf_wds_nip)
        sheet1.write('A210','V.')
        sheet1.merge_range('B210:H210','Catatan Ketua Tim Penilai:')
        sheet1.merge_range('B211:H224','')
        sheet1.write('I214','Bandung')
        sheet1.write('I215','Tim Penilai Angka Kredit-ITB')
        sheet1.write('I216','Ketua')
        sheet1.write('I220',conf_wrso_name)
        sheet1.write('I221',conf_wrso_nip)
        for i in range(29,189):
            for x in ['I','J','K','L','M','N']:
                sheet1.write(x + str(i),'',fmt_box)
        sheet1.write('J31',total['I.A.1'] if 'I.A.1' in total else '' )
        sheet1.write('J32',total['I.A.2'] if 'I.A.2' in total else '')
        sheet1.write('J34',total['I.B'] if 'I.B' in total else '')
        sheet1.write('J35','=SUM(J31:J34)')
        sheet1.write('J37',total['II.A'] if 'II.A' in total else '')
        sheet1.write('J38',total['II.B'] if 'II.B' in total else '')
        sheet1.write('J39',total['II.C'] if 'II.C' in total else '')
        #sheet1.write('J42',total['II.D.1.a'] if 'II.D.1.a' in total else '')
        #sheet1.write('J43',total['II.D.1.b'] if 'II.D.1.b' in total else '')
        #sheet1.write('J44',total['II.D.1.c'] if 'II.D.1.c' in total else '')
        #sheet1.write('J45',total['II.D.1.d'] if 'II.D.1.d' in total else '')
        #sheet1.write('J47',total['II.D.2.a'] if 'II.D.2.a' in total else '')
        #sheet1.write('J48',total['II.D.2.b'] if 'II.D.2.b' in total else '')
        #sheet1.write('J49',total['II.D.2.c'] if 'II.D.2.c' in total else '')
        #sheet1.write('J50',total['II.D.2.d'] if 'II.D.2.d' in total else '')
        sheet1.write('J52',total['II.E.1'] if 'II.E.1' in total else '')
        sheet1.write('J53',total['II.E.2'] if 'II.E.2' in total else '')
        sheet1.write('J54',total['II.F'] if 'II.F' in total else '')
        sheet1.write('J55',total['II.G'] if 'II.G' in total else '')
        sheet1.write('J57',total['II.H.1'] if 'II.H.1' in total else '')
        sheet1.write('J58',total['II.H.2'] if 'II.H.2' in total else '')
        sheet1.write('J59',total['II.I'] if 'II.I' in total else '')
        sheet1.write('J61',total['II.J.1'] if 'II.J.1' in total else '')
        sheet1.write('J62',total['II.J.2'] if 'II.J.2' in total else '')
        sheet1.write('J63',total['II.J.3'] if 'II.J.3' in total else '')
        sheet1.write('J64',total['II.J.4'] if 'II.J.4' in total else '')
        sheet1.write('J65',total['II.J.5'] if 'II.J.5' in total else '')
        sheet1.write('J66',total['II.J.6'] if 'II.J.6' in total else '')
        sheet1.write('J67',total['II.J.7'] if 'II.J.7' in total else '')
        sheet1.write('J68',total['II.J.8'] if 'II.J.8' in total else '')
        sheet1.write('J70',total['II.K.1'] if 'II.K.1' in total else '')
        sheet1.write('J71',total['II.K.2'] if 'II.K.2' in total else '')
        sheet1.write('J73',total['II.L.1'] if 'II.L.1' in total else '')
        sheet1.write('J74',total['II.L.2'] if 'II.L.2' in total else '')
        sheet1.write('J76',total['II.M.1'] if 'II.M.1' in total else '')
        sheet1.write('J77',total['II.M.2'] if 'II.M.2' in total else '')
        sheet1.write('J78',total['II.M.3'] if 'II.M.3' in total else '')
        sheet1.write('J79',total['II.M.4'] if 'II.M.4' in total else '')
        sheet1.write('J80',total['II.M.5'] if 'II.M.5' in total else '')
        sheet1.write('J81',total['II.M.6'] if 'II.M.6' in total else '')
        sheet1.write('J82',total['II.M.7'] if 'II.M.7' in total else '')
        sheet1.write('J83','=SUM(J37:J82)')
        sheet1.write('J88',total['III.A.1.a.1'] if 'III.A.1.a.1' in total else '')
        sheet1.write('J89',total['III.A.1.a.2'] if 'III.A.1.a.2' in total else '')
        sheet1.write('J91',total['III.A.1.b.1'] if 'III.A.1.b.1' in total else '')
        sheet1.write('J92',total['III.A.1.b.2'] if 'III.A.1.b.2' in total else '')
        sheet1.write('J93',total['III.A.1.b.3'] if 'III.A.1.b.3' in total else '')
        sheet1.write('J95',total['III.A.1.c.1.a'] if 'III.A.1.c.1.a' in total else '')
        sheet1.write('J96',total['III.A.1.c.1.b'] if 'III.A.1.c.1.b' in total else '')
        sheet1.write('J97',total['III.A.1.c.2.a'] if 'III.A.1.c.2.a' in total else '')
        sheet1.write('J98',total['III.A.1.c.2.b'] if 'III.A.1.c.2.b' in total else '')
        sheet1.write('J99',total['III.A.1.d'] if 'III.A.1.d' in total else '')
        sheet1.write('J100',total['III.A.2'] if 'III.A.2' in total else '')
        sheet1.write('J102',total['III.B'] if 'III.B' in total else '')
        sheet1.write('J104',total['III.C'] if 'III.C' in total else '')
        sheet1.write('J106',total['III.D.1'] if 'III.D.1' in total else '')
        sheet1.write('J107',total['III.D.2'] if 'III.D.2' in total else '')
        sheet1.write('J109',total['III.E.1'] if 'III.E.1' in total else '')
        sheet1.write('J110',total['III.E.2'] if 'III.E.2' in total else '')
        sheet1.write('J111',total['III.E.3'] if 'III.E.3' in total else '')
        sheet1.write('J112','=SUM(J88:J111)')
        sheet1.write('J115',total['IV.A'] if 'IV.A' in total else '')
        sheet1.write('J117',total['IV.B'] if 'IV.B' in total else '')
        sheet1.write('J121',total['IV.C.1.a.1'] if 'IV.C.1.a.1' in total else '')
        sheet1.write('J122',total['IV.C.1.a.2'] if 'IV.C.1.a.2' in total else '')
        sheet1.write('J123',total['IV.C.1.a.3'] if 'IV.C.1.a.3' in total else '')
        sheet1.write('J125',total['IV.C.1.b.1'] if 'IV.C.1.b.1' in total else '')
        sheet1.write('J126',total['IV.C.1.b.2'] if 'IV.C.1.b.2' in total else '')
        sheet1.write('J127',total['IV.C.1.b.3'] if 'IV.C.1.b.3' in total else '')
        sheet1.write('J128',total['IV.C.2'] if 'IV.C.2' in total else '')
        sheet1.write('J130',total['IV.D.1'] if 'IV.D.1' in total else '')
        sheet1.write('J131',total['IV.D.2'] if 'IV.D.2' in total else '')
        sheet1.write('J132',total['IV.D.3'] if 'IV.D.3' in total else '')
        sheet1.write('J134',total['IV.E'] if 'IV.E' in total else '')
        sheet1.write('J135','=SUM(J115:J134)')
        sheet1.write('J138',total['V.A.1'] if 'V.A.1' in total else '')
        sheet1.write('J139',total['V.A.2'] if 'V.A.2' in total else '')
        sheet1.write('J142',total['V.B.1.a'] if 'V.B.1.a' in total else '')
        sheet1.write('J143',total['V.B.1.b'] if 'V.B.1.b' in total else '')
        sheet1.write('J145',total['V.B.2.a'] if 'V.B.2.a' in total else '')
        sheet1.write('J146',total['V.B.2.b'] if 'V.B.2.b' in total else '')
        sheet1.write('J149',total['V.C.1.a'] if 'V.C.1.a' in total else '')
        sheet1.write('J150',total['V.C.1.b'] if 'V.C.1.b' in total else '')
        sheet1.write('J151',total['V.C.1.c'] if 'V.C.1.c' in total else '')
        sheet1.write('J153',total['V.C.2.a'] if 'V.C.2.a' in total else '')
        sheet1.write('J154',total['V.C.2.b'] if 'V.C.2.b' in total else '')
        sheet1.write('J155',total['V.C.2.c'] if 'V.C.2.c' in total else '')
        sheet1.write('J157',total['V.D'] if 'V.D' in total else '')
        sheet1.write('J159',total['V.E.1'] if 'V.E.1' in total else '')
        sheet1.write('J160',total['V.E.2'] if 'V.E.2' in total else '')
        sheet1.write('J163',total['V.F.1.a'] if 'V.F.1.a' in total else '')
        sheet1.write('J164',total['V.F.1.b'] if 'V.F.1.b' in total else '')
        sheet1.write('J166',total['V.F.2.a'] if 'V.F.2.a' in total else '')
        sheet1.write('J167',total['V.F.2.b'] if 'V.F.2.b' in total else '')
        sheet1.write('J170',total['V.G.1.a'] if 'V.G.1.a' in total else '')
        sheet1.write('J171',total['V.G.1.b'] if 'V.G.1.b' in total else '')
        sheet1.write('J172',total['V.G.1.c'] if 'V.G.1.c' in total else '')
        sheet1.write('J174',total['V.G.2.a'] if 'V.G.2.a' in total else '')
        sheet1.write('J175',total['V.G.2.b'] if 'V.G.2.b' in total else '')
        sheet1.write('J176',total['V.G.2.c'] if 'V.G.2.c' in total else '')
        sheet1.write('J178',total['V.H.1'] if 'V.H.1' in total else '')
        sheet1.write('J179',total['V.H.2'] if 'V.H.2' in total else '')
        sheet1.write('J180',total['V.H.3'] if 'V.H.3' in total else '')
        sheet1.write('J182',total['V.I.1'] if 'V.I.1' in total else '')
        sheet1.write('J183',total['V.I.2'] if 'V.I.2' in total else '')
        sheet1.write('J184',total['V.I.3'] if 'V.I.3' in total else '')
        sheet1.write('J186',total['V.J'] if 'V.J' in total else '')
        sheet1.write('J187','=SUM(J138:J186)')
        sheet1.write('J188','=J35+J83+J112+J135+J187',fmt_box)



DupakExcel('report.itb.dupak.xlsx','itb.dupak')

