import Vue from 'vue'
import VueRouter from 'vue-router'
import VueReactiveProvide from 'vue-reactive-provide'
import App from './App.vue'
import router from './router'
import './main.css'

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

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
