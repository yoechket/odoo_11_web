odoo.define('frontend_form.dyn_menu', function (require) {
'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var Widget = require('web.Widget');

    var navMenu = Widget.extend({
        startMenu: function(){
            var $sections = $(document).find('h1');
            var $titles = $.trim($sections.text());

            _.each($sections, function(el){
                var el_id = el.id
                var el_text = el.innerHTML;
                $("<li>").append($('<a href="#'+el_id+'"/>').text(el_text)).appendTo($('#side_menu'));
            });
        }
    });

    var nav_menu = new navMenu();
    nav_menu.startMenu();

});