import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import dashboardLayout from '@/pages/DashboardLayout'
import userIndex from '@/pages/user/user'
import userSettings from '@/pages/user/settings'

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
      component: dashboardLayout,
      children: [
        {
          path: '/user',
          component: userIndex,
          children: [
            { path: 'settings', name: 'settings', component: userSettings }
          ]
        }
      ]
    }
  ]
})
