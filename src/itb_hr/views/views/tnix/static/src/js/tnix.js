odoo.define('tnix', function (require) {
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
                this.$buttons.on('click', '.btn-allocate', this.proxy('allocate'));
                this.$buttons.on('click', '.btn-empty', this.proxy('empty'));
            }
        },
        allocate: function() {
            var mod = new Model('tnix.kandidat');
            mod.call('allocate',[[]]).done(this.proxy('reload_content'));
        },
        empty: function() {
            var mod = new Model('tnix.kandidat');
            mod.call('empty',[[]]).done(this.proxy('reload_content'));
        },
    });
})