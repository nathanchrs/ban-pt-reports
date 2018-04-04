from odoo import models, fields, api, exceptions
from odoo import http
    
    
class Abet(http.Controller):
    @http.route('/faculty', auth='public',website=True)
    def index(self, **kw):
        Teachers = http.request.env['itb.hr']
        return http.request.render('itb_hr.faculty_ind', {
            'teachers': Teachers.search([])
        })

class Website(http.Controller):
    '''
    @http.route('/index',auth='public',website=True)
    def list(self,**kw):
        hrs = http.request.env['itb.hr']
        print "Test is below "
        arr = hrs.search([])
        print arr
        return http.request.render('website.layout',
               {'hrs':hrs.search([])
     })
    '''
    @http.route('/template/', auth='public', website=True)
    def index(self, **kw):
        # return "Hello World"        
        hrs = http.request.env['itb.hr'].search([])
        return http.request.render('itb_hr.dosen_index', {
            'hrs': hrs,
            })
