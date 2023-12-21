# -*- coding: utf-8 -*-
{
    'name': "Customer Payment Report",

    'summary': """
        Customer Payment Report 
        """,

    'description': """
        Dynamic Customer Payment PDF Report Module 
    """,

    'author': "Ramsad PV",
    'category': 'Uncategorized',
    'version': '15.0.1',

    'depends': ['base','account','sale_management'],

    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/payment_report_wizard.xml',
    ],

}
