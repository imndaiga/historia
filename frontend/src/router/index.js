import Vue from 'vue'
import Router from 'vue-router'
import index from '@/pages/index'
import dashboardLayout from '@/pages/DashboardLayout'

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
    }
  ]
})
