from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail(self, auto_commit=False):
        if self._context.get('default_model') == 'sale.order' and self._context.get('default_res_id') and self._context.get('mark_so_as_sent'):
            order = self.env['sale.order'].browse([self._context['default_res_id']])
            if order.state == 'draft' and order.new_state == 'draft':
                order.with_context(tracking_disable=True).state = 'sent'
                order.with_context(tracking_disable=True).new_state = 'sent'
            elif order.new_state == 'approved':
                 order.with_context(tracking_disable=True).new_state = 'sent'
            self = self.with_context(mail_post_autofollow=True)
            # if order.new_state == 'approved':
            #     order.with_context(tracking_disable=True).new_state = 'sent'
            # self = self.with_context(mail_post_autofollow=True)
        return super(MailComposeMessage, self).send_mail(auto_commit=auto_commit)
