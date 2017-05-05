import Vue from 'vue'
import Router from 'vue-router'
import WelcomeView from '@/pages/WelcomeView'
import DashboardLayout from '@/pages/DashboardLayout'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: WelcomeView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardLayout
    }

  ]
})
