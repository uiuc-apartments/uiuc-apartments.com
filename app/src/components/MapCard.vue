<script lang="ts">
import leaflet from 'leaflet'
import type { Apartment } from '../types'

let map: leaflet.Map
let renderer: leaflet.Canvas
let markersLayer: leaflet.LayerGroup = leaflet.layerGroup()
let placed = new Map<string, leaflet.Marker>()

const fontAwesomeLocationDotSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 256c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"/></svg>'
const fontAwesomeIcon: leaflet.DivIcon = leaflet.divIcon({
    html: fontAwesomeLocationDotSvg,
    iconSize: [20, 20],
    className: 'marker-style'
});
export default {
  props: {
    apartments: {
      type: Object as () => Apartment[],
      required: true,
    },
  },
  emits: [
    'update:bounds'
  ],
  data() {
    return {}
  },
  watch: {
    apartments(newVal: Apartment[]) {
      markersLayer.clearLayers()
      placed.clear()
      // remove old layer if necessary
      if (map.hasLayer(markersLayer)) {
        map.removeLayer(markersLayer)
      }

      // console.log('newVal', newVal)
      // create new layer
      for (const apartment of newVal) {
        const location = leaflet.latLng(apartment.latitude, apartment.longitude)
        const description = `<a href="${apartment.link}" target="_blank" rel="noreferrer noopener">${apartment.address} - ${apartment.bedrooms} BR / ${apartment.bathrooms} BA - $${apartment.rent}</a>`
        var marker: leaflet.Marker | undefined;
        marker = placed.get(`${apartment.latitude},${apartment.longitude}`)
        if(marker !== undefined) {
          var currentPopup = marker.getPopup()?.getContent()
          marker.setPopupContent(currentPopup + "<br>" + description)
        } else {
          marker = leaflet
          .marker(location, {
            icon: fontAwesomeIcon,
          })
          .bindPopup(description)
          markersLayer.addLayer(marker)
        }
        placed.set(`${apartment.latitude},${apartment.longitude}`, marker);
      }
      // console.log('markersLayer', markersLayer)

      // add new layer
      markersLayer.addTo(map)
      // console.log(map)
    },
  },
  mounted() {
    // init map
    renderer = leaflet.canvas({ padding: 0.5 });
    map = leaflet
      .map('map', {
        zoomControl: true,
      }).addEventListener('moveend', (m) => {
        this.$emit('update:bounds', m.target.getBounds())
      })
      .setView([40.109, -88.227], 13) // illini union
    // add tile layers
    leaflet
      .tileLayer('https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=yvUGw3ndr6zJmLiXqkDi', {
        maxZoom: 18,
        attribution:
          '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>'
      })
      .addTo(map)
  },
}
</script>

<template>
  <div id="map"></div>
</template>

<style>
.marker-style {
  fill-opacity: 0.8;
  fill: blue;
}
#map {
  height: 600px;
}
</style>
