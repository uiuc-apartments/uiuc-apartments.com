import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faBath,
  faBed,
  faHome,
  faSignHanging,
  faLocationPin,
  faDollarSign,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons'
import {
  faGithub,
} from '@fortawesome/free-brands-svg-icons'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

import App from './App.vue'
import router from './router'

import './assets/main.css'
import './index.css'

library.add(faBath, faBed, faHome, faSignHanging, faLocationPin, faDollarSign, faChevronDown, faGithub)

const app = createApp(App)

app
  .use(router)
  .component('font-awesome-icon', FontAwesomeIcon)
  .component('Datepicker', Datepicker)

app.mount('#app')
