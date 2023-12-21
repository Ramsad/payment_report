from odoo import api, fields, models


class PaymentReportWizard(models.Model):
    _name = 'payment_report.wizard'
    _description = 'Payment Report Wizard'

    start_date = fields.Date(string="Start Date", required=False, )
    end_date = fields.Date(string="End Date", required=False, )

    def customer_payment_report(self):
        data = {'start_date': self.start_date, 'end_date': self.end_date,}
        return self.env.ref('payment_report.payment_report').report_action(self, data=data)


class SalesReport(models.AbstractModel):
    _name = 'report.payment_report.customer_payment_report_pdf'

    def get_report_details(self,start_date,end_date):

        # ORM method
        # invoice_ids = self.env['account.move'].search(
        #     [('invoice_date', '>=', start_date), ('invoice_date', '<=', end_date),('move_type','=','out_invoice')])
        # invoice_dict ={ }

        # SQL Query
        cr = self.env.cr
        sql = ('''SELECT l.id AS lid, l.partner_id AS partner_id,  l.invoice_date AS invoice_date, l.amount_total AS amount_total, \
                    l.amount_residual as balance_amount, p.name AS partner_name\
                    FROM account_move l\
                    LEFT JOIN res_partner p ON (l.partner_id=p.id)\
                    WHERE
                     l.move_type = 'out_invoice' AND l.invoice_date BETWEEN %(date_from)s AND %(date_to)s 
                     GROUP BY l.id,  l.invoice_date,p.name''')

        cr.execute(sql, {
                    'date_from': start_date,
                    'date_to': end_date
                })

        invoice_dict = {}
        for row in cr.dictfetchall():
            print(row['partner_id'])
            if row['partner_id'] in invoice_dict.keys():
                print("FFff")
                invoice_dict[row['partner_id']]['total_sale_count'] += 1
                invoice_dict[row['partner_id']]['total_amount'] += row['amount_total']
                invoice_dict[row['partner_id']]['balance_amount'] += row['balance_amount']
                if row['balance_amount'] :
                    invoice_dict[row['partner_id']]['paid_amount'] += row['amount_total'] - row['balance_amount']
                else:
                    invoice_dict[row['partner_id']]['paid_amount'] += row['amount_total']
            else :
                invoice_dict[row['partner_id']] = {
                    "name" : row['partner_name'],
                    "first_sale_date" : row['invoice_date'],
                    "total_sale_count" : 1,
                    "total_amount": row['amount_total'],
                    "balance_amount": row['balance_amount'],
                    "paid_amount": row['amount_total'] - row['balance_amount']
                }
        return {
            'invoices': invoice_dict,
        }

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        data.update(
            self.get_report_details(data['start_date'], data['end_date']))
        return data
