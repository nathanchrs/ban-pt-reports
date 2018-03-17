# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <record model="ir.ui.view" id="view_report_tree">
            <field name="name">Laporan</field>
            <field name="model">banpt_report_generator.report</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name" />
                    <field name="year" />
                    <field name="prodi" />
                </tree>
            </field>
        </record>
        <record model="ir.ui.view" id="view_report_form">
            <field name="name">Laporan</field>            
            <field name="model">banpt_report_generator.report</field>
            <field name="type">form</field>
            <field name="priority" eval="0" />
            <field name="arch" type="xml">
                <form string="Laporan">
                    <header>
                        <button string="Mutakhirkan data" type="object" name="refresh" />
                        <button string="Setujui" type="object" name="approve" attrs="{'invisible': [('state', '=', 'approved')]}" class="oe_highlight" />
                        <field name="state" widget="statusbar" />
                    </header>
                    <group>
                        <field name="id" invisible="1" />
                        <field name="name" />
                        <field name="year" attrs="{'readonly': [('id', '!=', False)]}" />
                        <field name="prodi" attrs="{'readonly': [('id', '!=', False)]}" />
                        <field name="description" />
                    </group>
                    <hr/>
                    <div class="banpt_notebook_group banpt_report_tables">
                        <div class="dropdown" id="banpt_report_tables_menu_container">
                            <a class="btn dropdown-toggle banpt_report_tables_menu" data-toggle="dropdown" href="#">
                                <span class="banpt_report_tables_menu_text">Pilih tabel </span><span class="caret"></span>
                            </a>
                            <ul class="dropdown-menu banpt_report_tables_dropdown" role="tablist">
                                <!-- Add table report dropdown menu items here -->
${dropdown_menu_items}
                            </ul>
                        </div>
                        <div class="tab-content">
                            <!-- Add table report contents here -->
${contents}
                        </div>
                    </div>
                </form>
            </field>
        </record>

        <record model="ir.actions.act_window" id="view_report_action">
            <field name="name">Laporan</field>
            <field name="res_model">banpt_report_generator.report</field>
            <field name="view_mode">tree,form</field>
            <field name="view_type">form</field>
            <field name="help" type="html">
                <p class="oe_view_nocontent_create">Belum ada laporan yang telah dibuat</p>
            </field>
        </record>

        <record model="ir.actions.act_window.view" id="view_report_tree_action">
            <field name="sequence" eval="0" />
            <field name="view_mode">tree</field>
            <field name="view_id" ref="view_report_tree" />
            <field name="act_window_id" ref="view_report_action" />
        </record>

        <record model="ir.actions.act_window.view" id="view_report_form_action">
            <field name="sequence" eval="1" />
            <field name="view_mode">form</field>
            <field name="view_id" ref="view_report_form" />
            <field name="act_window_id" ref="view_report_action" />
        </record>
    </data>
</odoo>
""")

dropdown_menu_item_template = string.Template(
"""                                <li role="presentation">
                                    <a href="#tab_${model_name}" aria-controls="tab_${model_name}" role="tab" data-toggle="tab">${model_title}</a>
                                </li>"""
)

content_template = string.Template(
"""                            <div role="tabpanel" class="tab-pane${is_active}" id="tab_${model_name}">
                                <h3 class="banpt_notebook_page_title">${model_title}</h3>
                                <field name="${model_name}" />
                            </div>"""
)

def generate_report_view(models, directory):
    dropdown_menu_items = []
    contents = []
    first_model = True
    for model in models:
        model_params = dict(model_name=model['name'], model_title=model['title'])
        dropdown_menu_items.append(dropdown_menu_item_template.substitute(model_params))

        # Only the first tab should be active
        model_params['is_active'] = ''
        if first_model: 
            model_params['is_active'] = ' active'
            first_model = False
        contents.append(content_template.substitute(model_params))

    view_template_params = dict(
        dropdown_menu_items=string.join(dropdown_menu_items, '\n'),
        contents=string.join(contents, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, 'report_views.xml')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
