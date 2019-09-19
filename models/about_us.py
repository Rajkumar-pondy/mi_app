# -*- coding: utf-8 -*-

from odoo import models, fields

class AboutUs(models.Model):
    _name="mi.aboutus"
    _rec_name='company_id'
    _description="About Us"
    
    company_id=fields.Many2one('res.company',string="Company Details")
    about=fields.Html(string="About")