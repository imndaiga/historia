import Vue from 'vue'
import Router from 'vue-router'
import WelcomeView from '@/components/WelcomeView'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'WelcomeView',
      component: WelcomeView
    }
  ]
})
