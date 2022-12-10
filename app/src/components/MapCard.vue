<script lang="ts">
import * as L from 'leaflet'
import 'leaflet.markercluster'
import 'leaflet-draw/dist/leaflet.draw.css'
import 'leaflet-draw/dist/leaflet.draw-src.css'
import 'leaflet-draw'
import type { Apartment } from '../types'

let map: L.Map
let renderer: L.Canvas
let markersLayer: L.FeatureGroup = L.markerClusterGroup({
  maxClusterRadius: function (zoom: number) {
    return zoom < 16 ? 20 : 5
  },
})

type MarkerInfo = {
  ids: number[]
  description: string
  location: L.LatLng
}
let placed = new Map<string, MarkerInfo>()

const fontAwesomeLocationDotSvg =
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Pro 6.2.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 256c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"/></svg>'
const fontAwesomeIconPerApartment: (ids: number[]) => L.DivIcon = (
  ids: number[]
) => {
  const classes = ids.map((id) => `marker-${id}`).join(' ')
  return L.divIcon({
    html: fontAwesomeLocationDotSvg,
    iconSize: [20, 20],
    className: `marker-style ${classes}`,
  })
}
/*
    .selected > 123 {

    }
  */
export default {
  props: {
    apartments: {
      type: Object as () => Apartment[],
      required: true,
    },
    selectedApartment: {
      type: Object as () => Apartment,
      required: true,
    },
  },
  emits: ['update:bounds', 'update:filter-shapes'],
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

      // first, build a lookup of location to data
      for (const apartment of newVal) {
        const location = L.latLng(apartment.latitude, apartment.longitude)
        const locationStr = `${apartment.latitude},${apartment.longitude}`
        const description = `<a href="${apartment.link}" target="_blank" rel="noreferrer noopener">${apartment.address} - ${apartment.bedrooms} BR / ${apartment.bathrooms} BA - $${apartment.rent}</a>`
        var markerInfo: MarkerInfo | undefined
        markerInfo = placed.get(locationStr)
        if (markerInfo !== undefined) {
          markerInfo.description += '<br>' + description
          markerInfo.ids.push(apartment.id)
        } else {
          markerInfo = { ids: [apartment.id], description, location }
        }
        placed.set(locationStr, markerInfo)
      }

      // loop over the lookup and add markers
      for (const [_, markerInfo] of placed) {
        const marker = L.marker(markerInfo.location, {
          icon: fontAwesomeIconPerApartment(markerInfo.ids),
        }).bindPopup(markerInfo.description)
        markersLayer.addLayer(marker)
      }

      // add new layer
      markersLayer.addTo(map)
    },
  },
  mounted() {
    // init map
    renderer = L.canvas({ padding: 0.5 })
    map = L.map('map', {
      zoomControl: true,
    })
      .addEventListener('moveend', (m) => {
        this.$emit('update:bounds', m.target.getBounds())
      })
      .setView([40.109, -88.227], 13) // illini union
    // add tile layers
    L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        maxZoom: 19,
        attribution:'&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
      }
    ).addTo(map)

    let editableLayers = new L.FeatureGroup()
    map.addLayer(editableLayers)

    const options: L.Control.DrawConstructorOptions = {
      draw: {
        polyline: false,
        marker: false,
        circlemarker: false,
        rectangle: false,
        circle: false,
      },
      edit: {
        featureGroup: editableLayers, //REQUIRED!!
      },
    }

    const drawControl = new L.Control.Draw(options)
    map.addControl(drawControl)

    map.on(L.Draw.Event.CREATED, (e) => {
      const layer = e.layer
      editableLayers.addLayer(layer)
    })

    map.on(Object.values(L.Draw.Event).join(' '), (e) => {
      const shapes = editableLayers.getLayers()
      console.log(shapes)
      this.$emit('update:filter-shapes', shapes)
    })
  },
}
</script>

<template>
  <div>
    <component is="style">
      .marker-{{ selectedApartment.id || 'no' }} { fill: red; }
    </component>
    <div id="map"></div>
  </div>
</template>

<style>
.marker-style {
  fill-opacity: 0.8;
  fill: blue;
}
#map {
  height: 600px;
}

.marker-cluster {
  display: flex;
  background: blue;
  opacity: 0.8;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: white;
  width: 20px !important;
  height: 20px !important;
}
</style>
