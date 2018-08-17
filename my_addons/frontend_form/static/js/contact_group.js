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

    var UpdateRankButton = Widget.extend({
        events: {
            'click': 'onClick',
        },
        onClick: function(ev){
            ev.preventDefault();
            var self = this;
            var href = this.$el.attr("href");
            var group_id = href.match(/group_id=([0-9]+)/);
            var token = href.match(/token=(.*)/);
            ajax.jsonRpc("/group/update_rank", 'call', {
                'group_id': parseInt(group_id[1]),
                'token': token[1],
                'increase': self.$el.is('[href*="increase"]'),
            }).then(function (data) {
                if(!data){
                    window.location.reload();
                }
                var rank_value = $(document).find(".js_rank").val();
                if(self.$el.children('span').attr('class') === 'fa fa-plus' && rank_value == 1){
                    alert('Max Rank Reached!');
                }
                else{
                    self.$el.parents('.input-group:first').find('.js_rank').val(data[0]);
                }
            });
            return false;
        },
    });

    var update_button_list = [];
    $('a.js_update_rank_json').each(function( index ) {
        var button = new UpdateRankButton();
        button.setElement($(this)).start();
        update_button_list.push(button);
    });

});