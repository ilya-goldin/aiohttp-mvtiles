if (!maplibregl.supported()) {
    alert("Your browser does not support Mapbox GL");
}

let map = new maplibregl.Map({
    container: "map",
    center: [0, 0],
    zoom: 1,
    style: {
        version: 8,
        name: "Main Layer",
    sources: {
        "aiohttp-mvtiles": {
            type: "vector",
            tiles: [
                "http://localhost:8080/api/v1/t.mvt?tile={z}/{x}/{y}",
                "http://localhost:8080/api/v1/tile/{z}/{x}/{y}" // Or like this
                ],
        }
    },
    layers: []
    },
})