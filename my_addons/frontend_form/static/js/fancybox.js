odoo.define('frontend_form.dyn_gallery', function (require) {
'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var config = require('web.config');
    var Widget = require('web.Widget');


    $("a.truesize_img").fancybox({
		'transitionIn'	:	'elastic',
		'transitionOut'	:	'elastic',
		'speedIn'		:	600,
		'speedOut'		:	200,
		'overlayShow'	:	false,
		'closeBtn'       :   true,
	});


});