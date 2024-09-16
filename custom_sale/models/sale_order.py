# coding: utf-8

from odoo import api, models, fields, _
from odoo.exceptions import UserError
from datetime import date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('submitted', 'Submitted to responsible'),
        ('to_send', 'Quotation to send'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ])

    def action_quotation_sent(self):
        if self.filtered(lambda so: so.state not in ['draft', 'submitted', 'to_send']):
            raise UserError(_('Only draft orders can be marked as sent directly.'))
        for order in self:
            order.message_subscribe(partner_ids=order.partner_id.ids)
        self.write({'state': 'sent'})

    def cron_auto_invoice_signed_purchase_contract(self):
        PurchaseContract = self.env['property.purchase_contract']
        SaleAdvancePaymentInv = self.env['sale.advance.payment.inv']

        today = date.today()
        purchase_contract_ids = PurchaseContract.search([
            ('is_real_signature', '=', True),
            ('signature_date', '<', today),
        ])
        sale_ids = self.search([
            ('state', '!=', 'cancel'),
            ('purchase_contract_id', 'in', purchase_contract_ids.ids),
        ])
        for sale_id in sale_ids.filtered(lambda x: not x.invoice_ids):
            if sale_id.state not in ('sale', 'sent'):
                sale_id.action_quotation_sent()
                sale_id.action_confirm()
            wizard_id = SaleAdvancePaymentInv.with_context(
                active_model=sale_id._name,
                active_id=sale_id.id,
                active_ids=sale_id.ids
            ).create({})
            print("\n\nwizard_id:::", wizard_id)
            wizard_id.create_invoices()

    def mark_quote_to_send(self):
        for sale_id in self:
            sale_id.state = 'to_send'

    def mark_submitted_at_manager(self):
        for sale_id in self:
            sale_id.state = 'submitted'

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'to_send').with_context(tracking_disable=True).write({'state': 'sent'})
        return super(SaleOrder, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    def get_invoices_amount_by_group(self):
        res = dict()
        for invoice_id in self.mapped('invoice_ids'):
            for tax_key, tax_data in invoice_id.tax_totals.get('groups_by_subtotal', {}).items():
                for tax_group in tax_data:
                    tax_name = tax_group.get('tax_group_name')
                    if tax_name not in res:
                        res[tax_name] = {
                            'base': 0,
                            'vat': 0,
                            'formatted_base': '0',
                            'formatted_vat': '0',
                        }
            amount_untaxed = invoice_id.tax_totals.get('amount_untaxed')
            res[tax_name]['base'] += amount_untaxed
            res[tax_name]['formatted_base'] = '%s %s' % (
                res[tax_name]['base'], invoice_id.currency_id.symbol)
            for subtotal_name, tax_groups in invoice_id.tax_totals.get('groups_by_subtotal', {}).items():
                for tax_group in tax_groups:
                    tax_group_amount = tax_group.get('tax_group_amount')
                    res[tax_name]['vat'] += tax_group_amount
                    res[tax_name]['formatted_vat'] = '%s %s' % (
                        res[tax_name]['vat'], invoice_id.currency_id.symbol)
        return res
