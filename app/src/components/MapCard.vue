<script lang="ts">
import leaflet from 'leaflet'
import type { Apartment } from '../types'

let map: leaflet.Map
let renderer: leaflet.Canvas
let markersLayer: leaflet.LayerGroup = leaflet.layerGroup()
let placed = new Map<string, leaflet.CircleMarker>()

export default {
  props: {
    apartments: {
      type: Object as () => Apartment[],
      required: true,
    },
  },
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

      console.log('newVal', newVal)
      // create new layer
      for (const apartment of newVal) {
        // TODO: the lat long was flipped in the DB, correcting it here
        const location = leaflet.latLng(apartment.longitude, apartment.latitude)
        const description = `${apartment.address} - ${apartment.bedrooms} BR / ${apartment.bathrooms} BA - $${apartment.rent}`
        var marker: leaflet.CircleMarker | undefined;
        marker = placed.get(`${apartment.latitude},${apartment.longitude}`)
        if(marker !== undefined) {
          var currentPopup = marker.getPopup()?.getContent()
          marker.setPopupContent(currentPopup + "<br>" + description)
        } else {
          marker = leaflet
            .circleMarker(location, {
              renderer: renderer
            })
            .bindPopup(description)
            markersLayer.addLayer(marker)
        }
        placed.set(`${apartment.latitude},${apartment.longitude}`, marker);
      }
      // console.log('markersLayer', markersLayer)

      // add new layer
      markersLayer.addTo(map)
      console.log(map)
    },
  },
  mounted() {
    // init map
    renderer = leaflet.canvas({ padding: 0.5 });
    map = leaflet
      .map('map', {
        zoomControl: true,
      })
      .setView([40.109, -88.227], 13) // illini union
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
  height: 600px;
}
</style>
