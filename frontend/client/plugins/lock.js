import Vue from 'vue'

const Auth0Lock = require('auth0-lock').default
const Lock = new Auth0Lock(process.env.clientID, process.env.clientDomain, allOptions())

function allOptions () {
  return {
    auth: {
      params: {
        scope: 'openid email'
      }
    }
  }
}

Lock.on('authenticated', function (authResult) {
  Lock.getUserInfo(authResult.accessToken, function (error, profile) {
    if (error) {
      return
    }
    localStorage.setItem('profile', JSON.stringify(profile))
    localStorage.setItem('id_token', authResult.idToken)
    Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
    console.log(Vue)
  })
})

Vue.prototype.lock = Lock
