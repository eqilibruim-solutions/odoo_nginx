odoo.define('awesome_template_widget.BasicRenderer', function (require) {
    "use strict";

    var core = require('web.core');
    const widgetRegistry = require('web.widget_registry');
    const widgetRegistryOwl = require("web.widgetRegistry");
    const WidgetWrapper = require("web.WidgetWrapper");

    const BasicRenderer = require('web.BasicRenderer');

    BasicRenderer.include({
        _renderWidget: function (record, node, options) {
            const name = node.attrs.name;
            const Widget = widgetRegistryOwl.get(name) || widgetRegistry.get(name);
            const legacy = !(Widget.prototype instanceof owl.Component);
            let widget;
            if (legacy) {
                widget = new Widget(this, record, node, _.extend({ mode: this.mode }, options || {}));
            } else {
                widget = new WidgetWrapper(this, Widget, {
                    record,
                    node,
                    options: _.extend({ mode: this.mode }, options || {})
                });
            }

            this.widgets.push(widget);

            // Prepare widget rendering and save the related promise
            let def;
            if (legacy) {
                def = widget._widgetRenderAndInsert(function () { });
            } else {
                def = widget.mount(document.createDocumentFragment());
            }
            this.defs.push(def);
            var $el = $('<div>');

            var self = this;
            def.then(function () {
                self._handleAttributes(widget.$el, node);
                self._registerModifiers(node, record, widget);
                widget.$el.addClass('o_widget');
                $el.replaceWith(widget.$el);
            });

            return $el;
        }
    })
})