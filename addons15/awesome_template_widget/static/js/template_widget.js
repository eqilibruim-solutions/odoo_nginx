odoo.define("awesome.template_widget", function (require) {
    "use strict";

    var registry = require("web.widget_registry");
    var core = require('web.core');
    var config = require('web.config')
    var Widget = require("web.Widget")
    var py = require('web.py_utils')

    var qweb = core.qweb;

    var awesome_template_widget = Widget.extend({

        events: _.extend({}, Widget.prototype.events, {
            "click button": "_on_button_click",
        }),

        init: function (parent, record, node, options) {
            this.record = record
            this.options = py.py_eval(node.attrs.options || '{}')
            this.options = _.extend({}, this.options || {}, options || {})
            this.template = this.options.template || undefined;
            this.node = node
            return this._super.apply(this, arguments);
        },

        _on_button_click: function (e) {
            var self = this;
            var $target = $(e.currentTarget)

            e.stopPropagation();
            self.trigger_up('button_clicked', {
                attrs: {
                    name: $target.attr('name'),
                    type: $target.attr('type'),
                    special: $target.attr('special') || '',
                    context: py.py_eval($target.attr('context') || '{}')
                },
                record: this.record,
            });
        },

        _render: function () {
            var $el = undefined;
            if (this.template) {
                $el = $(qweb.render(this.template, { widget: this, debug: config.debug }));
            } else {
                $el = this._super.apply(this)
            }
            this._replaceElement($el);

            // bind the dropdown
            this.$('.dropdown-toggle').dropdown()
        }
    });

    registry.add("awesome_template_widget", awesome_template_widget);

    return awesome_template_widget
});
