import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import dashboardTemplate from '@/templates/dashboard'
import userIndex from '@/pages/user/user'
import userSettings from '@/pages/user/settings'
import userHome from '@/pages/user/home'
import visualisation from '@/pages/visualisation'
import relationships from '@/pages/relationships'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: index
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: dashboardTemplate,
      children: [
        {
          path: '/user',
          name: 'user',
          component: userIndex,
          children: [
            { path: 'settings', name: 'settings', component: userSettings },
            { path: 'home', name: 'home', component: userHome }
          ]
        },
        {
          path: '/visualisation',
          name: 'visualisation',
          component: visualisation
        },
        {
          path: '/relationships',
          name: 'relationships',
          component: relationships
        }
      ]
    }
  ]
})
