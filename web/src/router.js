import VueRouter from "vue-router";
import store from './store'

const router = new VueRouter({
  mode: 'history',
  routes: [
    { name: 'sites', path: '/sites', component: () => import('./views/sites/list') },
    { name: 'new_site', path: '/sites/new', component: () => import('./views/sites/new') },
    { name: 'site', path: '/sites/:id', component: () => import('./views/sites/show') },
    { name: 'magnets', path: '/magnets', component: () => import('./views/magnets/list') },
    { name: 'new_magnet', path: '/magnets/new', component: () => import('./views/magnets/new') },
    { name: 'magnet', path: '/magnets/:id', component: () => import('./views/magnets/show') },
    { name: 'materials', path: '/materials', component: () => import('./views/materials/list') },
    { name: 'new_material', path: '/materials/new', component: () => import('./views/materials/new') },
    { name: 'material', path: '/materials/:id', component: () => import('./views/materials/show') },
    { name: 'parts', path: '/parts', component: () => import('./views/parts/list') },
    { name: 'new_part', path: '/parts/new', component: () => import('./views/parts/new') },
    { name: 'part', path: '/parts/:id', component: () => import('./views/parts/show') },
    { name: 'root', path: '/', component: () => import('./views/root') },
    { name: 'sign_in', path: '/sign_in', component: () => import('./views/signin') }
  ]
})

router.beforeEach(async (to, _, next) => {
  if (to.name !== 'sign_in' && !store.getters.isLogged) {
    return next({ name: 'sign_in' })
  }
  return next()
})

export default router
