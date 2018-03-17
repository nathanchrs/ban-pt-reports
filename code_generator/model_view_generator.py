# -*- coding: utf-8 -*-

import string
from os import path

view_template = string.Template(
"""<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>
        <record model="ir.ui.view" id="view_${name}_tree">
            <field name="name">${title}</field>
            <field name="model">banpt_report_generator.${name}</field>
            <field name="type">tree</field>
            <field name="arch" type="xml">
                <tree editable="bottom" decoration-info="write_date > report_refresh_date">
                    <field name="write_date" invisible="1" />
                    <field name="report_refresh_date" invisible="1" />
${tree_fields}
                </tree>
            </field>
        </record>

        <record model="ir.ui.view" id="view_${name}_form">
            <field name="name">${title}</field>
            <field name="model">banpt_report_generator.${name}</field>
            <field name="type">form</field>
            <field name="arch" type="xml">
                <form string="${title}">
                    <group>
${form_fields}
                    </group>
                </form>
            </field>
        </record>

         <record model="ir.actions.act_window" id="view_${name}_action">
            <field name="name">${title}</field>
            <field name="res_model">banpt_report_generator.${name}</field>
            <field name="view_mode">tree,form</field>
            <field name="view_type">form</field>
        </record>

        <record model="ir.actions.act_window.view" id="view_${name}_tree_action">
            <field name="sequence" eval="0" />
            <field name="view_mode">tree</field>
            <field name="view_id" ref="view_${name}_tree" />
            <field name="act_window_id" ref="view_${name}_action" />
        </record>

        <record model="ir.actions.act_window.view" id="view_${name}_form_action">
            <field name="sequence" eval="1" />
            <field name="view_mode">form</field>
            <field name="view_id" ref="view_${name}_form" />
            <field name="act_window_id" ref="view_${name}_action" />
        </record>
    </data>
</odoo>
""")

tree_field_template = string.Template('                    <field name="$field_name" />')
form_field_template = string.Template('                        <field name="$field_name" />')

def generate_model_view(name, title, fields, directory):
    tree_fields = []
    form_fields = []
    for field in fields:
        if field != 'report' and field != 'report_refresh_date':
            tree_fields.append(tree_field_template.substitute(dict(field_name=field)))
            form_fields.append(form_field_template.substitute(dict(field_name=field)))

    view_template_params = dict(
        name=name,
        title=title,
        tree_fields=string.join(tree_fields, '\n'),
        form_fields=string.join(form_fields, '\n')
    )
    generated_view = view_template.substitute(view_template_params)

    view_path = path.join(directory, name + '_views.xml')
    with open(view_path, 'w') as fout:
        fout.write(generated_view)
