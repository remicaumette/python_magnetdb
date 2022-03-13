import { Chart, registerables } from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import Vue from 'vue'
import VueRouter from 'vue-router'
import VueReactiveProvide from 'vue-reactive-provide'
import App from './App.vue'
import router from './router'
import store from './store'
import './main.css'

Chart.register(...registerables, zoomPlugin)

Vue.config.productionTip = false
Vue.use(VueReactiveProvide)
Vue.use(VueRouter)

Vue.filter('datetime', (date) => {
  if (!date) {
    return
  }

  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
  }).format(date instanceof Date ? date : new Date(date))
})

Vue.filter('statusName', (status) => status)

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
