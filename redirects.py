urls = (
    ('/video-tour', '/tour'),
    ('/virtual-tour-2', '/tour'),
    ('/contact-us', '/contact'),
    ('/wood-sense', '/about'),
    ('/testimonials', '/reviews'),

    ('/dining-tables', '/category/dining/dining-tables'),
    ('/chairs', '/category/dining/chairs'),
    ('/buffets', '/category/dining/buffets'),
    ('/cabinets', '/category/dining/cabinets'),
    ('/wine-racks-and-bar-counters', '/category/dining/wine-racks-bar-counters'),

    ('/coffee-tables', '/category/living/coffee-tables'),
    ('/side-tables', '/category/living/side-tables'),
    ('/console-table', '/category/living/console-table'),
    ('/desks', '/category/living/desks'),
    ('/tv-entertainment-units', '/category/living/tv-entertainment-units'),
    ('/benches-and-stools', '/category/living/benches-and-stools'),
    ('/accent-chairs', '/category/living/accent-chairs'),
    ('/bookcases', '/category/living/bookcases'),
    ('/doors-and-gazebos', '/category/living/doors-and-gazebos'),

    ('/beds', '/category/bedroom/beds'),
    ('/night-tables', '/category/bedroom/night-tables'),
    ('/dressers', '/category/bedroom/dressers'),
    ('/chests', '/category/bedroom/chests'),
    ('/armoires', '/category/bedroom/armoires'),

    ('/one-of-a-kind-single-vanities', '/category/vanities-sinks/one-of-a-kind-single-vanities'),
    ('/one-of-a-kind-double-vanities', '/category/vanities-sinks/one-of-a-kind-double-vanities'),
    ('/modern-single-vanity', '/category/vanities-sinks/modern-single-vanity'),
    ('/modern-double-vanity', '/category/vanities-sinks/modern-double-vanity'),
    ('/stone-sinks', '/category/vanities-sinks/stone-sinks'),
    ('/faucets', '/category/vanities-sinks/faucets'),
    ('/shower-heads', '/category/vanities-sinks/shower-heads'),

    ('/ceiling-lights', '/category/lighting/ceiling-lights'),
    ('/floor-lamps', '/category/lighting/floor-lamps'),
    ('/candle-stands-more', '/category/lighting/candle-stands-more'),
    ('/wall-lights', '/category/vanities-sinks/shower-heads'),

    ('/metal-art-paintings', '/category/accesories/metal-art-paintings'),
    ('/mirrors', '/category/accesories/mirrors'),
    ('/statues', '/category/accesories/statues'),
    ('/drapes', '/category/accesories/drapes'),
    ('/wall-panels-and-carved-panels', '/category/accesories/wall-panels-and-carved-panels'),
    ('/hooks', '/category/accesories/hooks'),
    ('/boxes-trinkets', '/category/accesories/boxes-trinkets'),
)

for old, new in urls:
    print("rewrite ^%s$ %s permanent;" % (old, new))
