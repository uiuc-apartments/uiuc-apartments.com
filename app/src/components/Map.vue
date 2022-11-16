<script>
import leaflet from 'leaflet'
export default {
  data() {
    return {}
  },
  mounted() {
    // init map
    let map = leaflet
      .map('map', {
        zoomControl: true,
      })
      .setView([28.538336, -81.379234], 10)
    // add tile layers
    leaflet
      .tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution:
          '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      })
      .addTo(map)
  },
}
</script>

<template>
  <div id="map"></div>
</template>

<style>
 #map {
  height: 300px;
 }
</style>
