# -*- coding: utf-8 -*-
{
    'name': 'Website Form',

    'author': 'Youssef Echcherif El Kettani',

    'summary': "Sandbox for frontend forms",

    'depends': ['website',
                'portal',
                'contacts',
                'smile_menu_icon_10',
                'calendar',
                'crm',
                'sale_management',
                'account_invoicing',
                'point_of_sale',
                'stock'],

    'data': ['data/menu_icons.xml',
             'report/contact_group_report.xml',
             'security/ir.model.access.csv',
             'views/add_contact_templates.xml',
             'views/home_page.xml',
             'views/assets.xml',
             'views/contact_extension.xml',
             'views/contact_group.xml',
             'views/contact_group_template.xml',
             'views/website_layout.xml',
             'views/fancybox_snippet.xml',
             ],
}