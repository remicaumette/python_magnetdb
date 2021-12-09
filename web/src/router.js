import VueRouter from "vue-router";

const router = new VueRouter({
  mode: 'history',
  routes: [
    { name: 'sites', path: '/sites', component: () => import('./views/sites/list') },
    { name: 'new_site', path: '/sites/new', component: () => import('./views/sites/new') },
    { name: 'site', path: '/sites/:id', component: () => import('./views/sites/show') },
    { name: 'magnets', path: '/magnets', component: () => import('./views/sites/list') },
    { name: 'parts', path: '/parts', component: () => import('./views/sites/list') },
    { name: 'materials', path: '/materials', component: () => import('./views/sites/list') },
    { name: 'records', path: '/records', component: () => import('./views/sites/list') },
  ]
})

export default router
