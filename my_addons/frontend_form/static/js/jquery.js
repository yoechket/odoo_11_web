odoo.define('frontend_form.toggle_form', function (require) {
'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var Widget = require('web.Widget');

    const $buttonToggleForm = $('#toggleForm');
    const $contactForm = $('#contact_form');

    $(document).ready(function(){
        $contactForm.hide();
    });

    $buttonToggleForm.on('click', () => {
        $contactForm.slideToggle(1000);
        var text = ($.trim($buttonToggleForm.html()) == "Show Form") ? "Hide Form" : "Show Form";
        $buttonToggleForm.html(text);
    });

});