# -*- coding: utf-8 -*-

from odoo import models, fields

class AboutUs(models.Model):
    _name="mi.aboutus"
    
    company_id=fields.Many2one('res.company',string="Company Details")