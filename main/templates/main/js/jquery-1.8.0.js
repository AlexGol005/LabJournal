$(document).ready( function() {
$('.dropdown-toggle').dropdown();
});
(function(window, $){
    var $window = $(window),
        isWindowLoad = false;
    $window.on('load', function(){
        isWindowLoad = true;
    });
    function log(){
        console.log.apply(console, arguments);
    }
    $(document).ready(function(){
        function initMenu(){
            var $hNav = $('#stick_menu'); /*ID фиксируемого элемента*/
            function checkScroll(e, init){
                init = init || false;
                if ($window.scrollTop() > 120) { /*Высота срабатывания*/
                    if ($('#navbar').is(':hidden')) { /*Триггер переключения*/
                    $hNav.addClass('fixed-top');}
                } else {
                    $hNav.removeClass('fixed-top');
                }
            }
            checkScroll(null, true);
            $window.on('scroll.checkScroll', checkScroll);
        }
       initMenu();
    });
}(window, window.jQuery));