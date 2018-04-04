odoo.define('itb_plan', function (require) {
   "use strict";
   var ListView = require('web.ListView');
   var Model = require('web.DataModel');

   ListView.include({
       init : function() {
           this._super.apply(this, arguments);
       },
       render_buttons: function(){
           this._super.apply(this, arguments);
           if (this.$buttons) {
               this.$buttons.on('click', '.btn-generateplan', this.proxy('generateplan'));
               this.$buttons.on('click', '.btn-sendrequest', this.proxy('tree_view_action'));
           }
       },
       generateplan: function() {
           var mod = new Model('itb.plan_int');
           mod.call('generateplan',[[]]).done(this.proxy('reload_content'));
       },

       tree_view_action: function () {           
        
        this.do_action({               
            type: "ir.actions.act_window",               
            name: "Send DKO to request",               
            res_model: "itb.plan_dko_wizard",               
            views: [[false,'form']],               
            target: 'new',               
            view_type : 'form',               
            view_mode : 'form',
            context: {'parent_id': self.ids}               
            //flags: {'form': {'action_buttons': False, 'options': {'mode': 'edit'}}}
        });
        return { 'type': 'ir.actions.client','tag': 'reload', } },

       sendrequest: function() {
           var mod = new Model('itb.plan_dko');
           mod.call('sendrequest',[[]]).done(this.proxy('reload_content'));
       },
   });
})
