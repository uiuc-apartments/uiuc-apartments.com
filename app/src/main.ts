import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import vuetify from './plugins/vuetify'
import {
  faBath,
  faBed,
  faHome,
  faSignHanging,
  faLocationPin,
  faDollarSign,
} from '@fortawesome/free-solid-svg-icons'

import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import './index.css'

library.add(faBath, faBed, faHome, faSignHanging, faLocationPin, faDollarSign)

const app = createApp(App)

app
  .use(router)
  .use(vuetify)
  .component('font-awesome-icon', FontAwesomeIcon)
  .component('Datepicker', Datepicker)

app.mount('#app')
