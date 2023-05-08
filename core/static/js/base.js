function setCookie(name, value, days) {
    var expires;

    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + expires + "; path=/";
}

function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (i; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $('#btn-top-search').popover({
        content: '<form method="GET" action="/search" id="form-top-search"><input type="text" class="form-control form-control-sm" name="q" placeholder="Search"></form>',
        html: true,
        //trigger: 'manual',
        placement: 'bottom'
    });
    $('#btn-top-search').on('shown.bs.popover', function () {
        $('#form-top-search input').focus();
    });

    // MOBILE MENU
    function init_mobile_menu() {
        $("#main-menu").mmenu({
            // options
        }, {
            // configuration
            // offCanvas: {
            //     pageSelector: "#wrapper"
            // }
        });
    }

    // DESKTOP MENU
    function init_desktop_menu() {

        function close_all_submenus() {
            var $links_to_close = $('.navi .opened-link');
            $links_to_close.find('.fa').removeClass('fa-angle-up').addClass('fa-angle-down');
            $links_to_close.removeClass('opened-link');

            // Close all common submenus
            var $submenus_to_close = $links_to_close.find('~ .opened-submenu');
            $submenus_to_close.hide();
            $submenus_to_close.removeClass('opened-submenu');

            // if (!$link || ($link && $link.not('#products-link'))) {
            //     console.log('close cat')
            // Close categories submenu
            var $categories_submenu = $('#categories-submenu');
            $categories_submenu.hide();
            $categories_submenu.removeClass('opened-submenu');
            // }
        }

        var $navi_li = $('.navi > li');
        //
        $navi_li.has('> ul').find('> a').append($('<i>').addClass('ml-1 fa fa-angle-down'));

        // SUBMENU LINK CLICK
        $navi_li.has('> ul').find('> a').add('#products-link').click(function (e) {
            e.stopPropagation();
            var $this = $(this);
            //
            if ($this.hasClass('opened-link')) {
                // Close
                close_all_submenus();
            } else {
                close_all_submenus($(this));
                // Open
                $this.addClass('opened-link');
                $this.find('.fa').removeClass('fa-angle-down').addClass('fa-angle-up');
                if ($this.is('#products-link')) {
                    var $submenu = $('#categories-submenu');
                } else {
                    var $submenu = $this.parent().find('> ul');
                }
                // Show submenu
                $submenu.show();
                $submenu.toggleClass('opened-submenu');
                //
                //close_all_submenus($this);
            }

            return false;
        });

        // CLOSE ALL SUBMENUS WHEN CLICK OUTSIDE IS PERFORMED
        $('body').click(function () {
            close_all_submenus();
        });
    }

    function init_menus() {
        if ($(window).width() <= 992) {
            init_mobile_menu();
        } else {
            init_desktop_menu();
        }
    }

    init_menus();

    // SHOW MORE
    // Configure/customize these variables.
    var showChar = 200;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "Read More";
    var lesstext = "Show Less";


    $('.more').each(function () {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });

    $(".morelink").click(function () {
        if ($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });

    // $(window).on('resize', function () {
    //     init_menus()
    // });
});
