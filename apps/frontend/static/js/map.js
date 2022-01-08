if (!maplibregl.supported()) {
    alert('Your browser does not support Mapbox GL');
}

let map = new maplibregl.Map({
    container: 'map',
    hash: true,
    style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
    center: [19, 47.8],
    zoom: 3.75,
    pitch: 0,
})

map.on('load', function () {
    map.resize()
})