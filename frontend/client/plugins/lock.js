import Vue from 'vue'
const Auth0Lock = require('auth0-lock').default
const store = require('~store').default
const router = require('~router').default

const options = {
  auth: {
    params: {
      scope: 'openid email'
    }
  }
}

const Lock = new Auth0Lock(process.env.clientID, process.env.clientDomain, options)

Lock.on('authenticated', function (authResult) {
  Lock.getUserInfo(authResult.accessToken, function (error, profile) {
    if (error) {
      return
    }
    localStorage.setItem('id_token', authResult.idToken)
    localStorage.setItem('profile', profile)
    store.dispatch('login', JSON.stringify(profile))
    Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
    router.push('/user/home')
  })
})

Vue.prototype.lock = Lock
