from odoo import models, fields, api

PROCUREMENT_PRIORITIES = [('0', 'Not urgent'), ('1', 'Normal'), ('2', 'Urgent'), ('3', 'Very Urgent')]

class TestReport(models.TransientModel):
    _name = 'mi.test.report'
    _description = "The wizard"

   
    priority = fields.Selection(PROCUREMENT_PRIORITIES, 'Priority', default='1')
    discount_id = fields.Many2one('mi.sale.order', string="Products")
    discount = fields.Float()
  
    @api.multi
    def change_discount(self):
        if self.discount_id:
            self.discount_id.discount = self.discount
            self.discount_id.priority = self.priority
            return True
