import Vue from 'vue'
import VueRouter from 'vue-router'
import VueReactiveProvide from 'vue-reactive-provide'
import App from './App.vue'
import router from './router'
import './main.css'

Vue.config.productionTip = false
Vue.use(VueReactiveProvide)
Vue.use(VueRouter)

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
