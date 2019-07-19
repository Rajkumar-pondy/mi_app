from odoo import models, fields, api

PROCUREMENT_PRIORITIES = [('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')]

class TestReport(models.TransientModel):
    _name = 'mi.test.report'

   
    priority = fields.Selection(PROCUREMENT_PRIORITIES, 'Priority', default='1')
  
    @api.multi
    def get_priority(self):
        return True