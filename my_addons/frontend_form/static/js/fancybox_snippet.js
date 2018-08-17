odoo.define('frontend_form.fancybox_snippet', function (require) {
'use strict';

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var widgets = require('web_editor.widget');
    var options = require('web_editor.snippets.options');

    var _t = core._t;
    var qweb = core.qweb;

    options.registry.fancybox = options.Class.extend({

        /**
         * @override
         */
        start: function () {
            var self = this;

            // The snippet should not be editable
            this.$target.attr('contentEditable', false);

            // Make sure image previews are updated if images are changed
            this.$target.on('save', 'img', function (ev) {
                var $img = $(ev.currentTarget);
                var index = self.$target.find('.item.active').index();
                /*self.$('.carousel:first li[data-target]:eq(' + index + ')')
                    .css('background-image', 'url(' + $img.attr('src') + ')');*/
            });

            // When the snippet is empty, an edition button is the default content
            // TODO find a nicer way to do that to have editor style
            this.$target.on('click', '.o_add_images', function (e) {
                e.stopImmediatePropagation();
                self.addImages(false);
            });

            return this._super.apply(this, arguments);
        },

        addImages: function (previewMode) {
            var self = this;
            var $row = $('<div/>', {class: 'row'});
            var $container = this.$('.container:first');
            var imgs = this._getImages();
            var dialog = new widgets.MediaDialog(this, {select_images: true}, this.$target.closest('.o_editable'), null);
            var lastImage = _.last(imgs);
            var index = lastImage ? this._getIndex(lastImage) : -1;

            dialog.on('save', this, function (attachments) {
                for (var i = 0 ; i < attachments.length; i++) {
                    $('<a/>', {
                        class: 'truesize_img',
                        href: attachments[i].src,
                        'data-index': ++index,
                    }).append($('<img/>', {
                                class: 'thumbnail_group',
                                src: attachments[i].src,})).appendTo($container);
                }
                self._reset();
                self.trigger_up('cover_update');
            });
            dialog.open();
            this._replaceContent($row);
        },

        mode: function (previewMode, value, $li) {
            this.$target.css('height', '');
            this[value]();
            this.$target
                .removeClass('o_nomode')
                .addClass('o_' + value);
        },

        nomode: function () {
            var $row = $('<div/>', {class: 'row'});
            var imgs = this._getImages();

            this._replaceContent($row);

            _.each(imgs, function (img) {
                var wrapClass = 'col-md-3';
                if (img.width >= img.height * 2 || img.width > 600) {
                    wrapClass = 'col-md-6';
                }
                var $wrap = $('<div/>', {class: wrapClass}).append(img);
                $row.append($wrap);
            });
        },

        _replaceContent: function ($content) {
            var $container = this.$('.container:first');
            $container.empty().append($content);
            return $container;
        },

        _getIndex: function (img) {
            return img.dataset.index || 0;
        },

        _getImages: function () {
            var imgs = this.$('img').get();
            var self = this;
            imgs.sort(function (a, b) {
                return self._getIndex(a) - self._getIndex(b);
            });
            return imgs;
        },
    });
});