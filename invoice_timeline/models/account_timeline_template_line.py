# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta
from odoo import api, models, _, fields
from odoo.exceptions import UserError


def increment_date(date, interval, interval_type):
    """ Increments the given date by a specified interval based on the interval_type """
    if interval:
        if interval_type == 'day':
            return date + relativedelta(days=interval)
        elif interval_type == 'month':
            return date + relativedelta(months=interval)
    return date  # Return the original date if interval is None or 0.


def decrement_date(date, interval, interval_type):
    """ Decrements the given date by a specified interval based on the interval_type """
    if interval:
        if interval_type == 'day':
            return date - relativedelta(days=interval)
        elif interval_type == 'month':
            return date - relativedelta(months=interval)
    return date  # Return the original date if interval is None or 0.


class AccountTimelineTemplateLine(models.Model):
    _name = 'account.timeline.template.line'
    _description = _('Account timeline template line')
    _order = 'sequence'

    interval = fields.Integer(_('Interval'))
    interval_type = fields.Selection([
        ('day', _('Day')),
        ('month', _('Month')),
    ], string=_('Interval type'), required=True, default='day')
    percent = fields.Float(_('Percent'), required=True, default=100)
    sequence = fields.Integer(_('Sequence'), compute='_cpt_sequence', store=True)
    product_categ_id = fields.Many2one('product.category', string=_('Product category'), help=_("""
           When you choose a product category, it will exclude it from the global invoiceable price
           Then it will create specific invoice line for this product category and assiocated percentage
       """))
    template_id = fields.Many2one('account.timeline.template', string=_('Template'), required=True, ondelete='cascade')

    @api.depends('interval_type', 'interval')
    def _compute_sequence(self):
        """ Computes the sequence based on the interval and interval_type. If interval_type is 'month', the sequence
        is multiplied by 31 """
        for record in self:
            record.sequence = record.interval
            if record.interval_type == 'month':
                record.sequence *= 31

    @api.constrains('percent')
    def _check_percent_constraints(self):
        """ Ensures that the 'percent' field value is within the valid range (0-100) """
        for record in self:
            if record.percent < 0:
                raise UserError(_('Percent must be positive! (Currently: %s)') % record.percent)
            elif record.percent > 100:
                raise UserError(_('Percent must be less than or equal to 100! (Currently: %s)') % record.percent)

    def _get_date(self, date_start):
        """
        Compute a list of dates starting from `date_start`,
        incrementing based on line intervals.

        Returns: list
        """
        real_date_start = decrement_date(date_start, self.interval, self.interval_type)
        line_ids = self.template_id.line_ids.filtered(lambda l: l.sequence >= self.sequence and l != self)
        line_ids = line_ids.sorted('sequence')
        dates = [date_start]
        for line_id in line_ids:
            date = increment_date(real_date_start, line_id.interval, line_id.interval_type)
            if date not in dates:
                dates.append(date)
        return dates
