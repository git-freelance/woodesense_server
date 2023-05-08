$(function () {

    // SHOWROOM
    var IMAGES = 6;
    var all_gallery_images_length = all_gallery_images.length;
    var $containers = $('.showroom .img-box');
    var current_image_index = 0;
    var current_position_index = 0;

    var positions = _.shuffle(_.range(IMAGES));

    function generate_next_image_src() {
        var ret = all_gallery_images[current_image_index];
        current_image_index < all_gallery_images_length - 1 ? current_image_index++ : current_image_index = 0;

        return ret;
    }

    $containers.each(function () {
        // init
        var next_image = generate_next_image_src();
        $(this).attr('href', next_image);
        $(this).find('img').attr('src', next_image);
    });

    // Init next image
    function get_next_image(){
        return $('<img />').attr('src', generate_next_image_src());
    }

    var $preloaded_next_image = get_next_image();

    function changeImage() {
        var $img = $('.showroom .col-img').eq(positions[current_position_index]).find('img');
        $img.fadeOut(function () {
            var next_image_src = $preloaded_next_image.attr('src');
            if ($(this).attr('src') === next_image_src) {
                // If random image is the same image, generate new random
                // next_image = get_next_image();
                $preloaded_next_image = get_next_image();
                next_image_src = $preloaded_next_image.attr('src');
            }
            $(this).parent().attr('href', next_image_src);
            $(this).attr('src', next_image_src).fadeIn();
            current_position_index < positions.length - 1 ? current_position_index++ : current_position_index = 0;
            $preloaded_next_image = get_next_image();
        });
    }

    setInterval(changeImage, 2500);
});