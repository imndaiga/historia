import Auth0Lock from 'Auth0Lock'
import router from '../router'
import axios from 'axios'

var lockOptions = {
  auth: {
    params: {
      scope: 'openid email'
    }
  }
}

var id = process.env.AUTH0_ID
var domain = process.env.AUTH0_DOMAIN
const lock = new Auth0Lock(id, domain, lockOptions)

lock.on('authenticated', function (authResult) {
  lock.getUserInfo(authResult.accessToken, function (error, profile) {
    if (error) {
      // Handle error
      console.log('Error loading the Profile', error)
      return
    }
    localStorage.setItem('id_token', authResult.idToken)
    localStorage.setItem('profile', JSON.stringify(profile))
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
    router.replace({name: 'home'})
  })
})

if (localStorage.getItem('id_token')) {
  axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
}

var login = function () {
  lock.show()
}

var logout = function () {
  localStorage.removeItem('id_token')
  localStorage.removeItem('profile')
}

var checkAuth = function () {
  if (localStorage.getItem('id_token')) {
    return true
  } else {
    return false
  }
}

var requireAuth = function (to, from, next) {
  if (!checkAuth()) {
    console.log('frontend client says: unauthorised!')
    var path = '/'
    next({ path: path })
  } else {
    next()
  }
}

var autoRoute = function (to, from, next) {
  if (checkAuth()) {
    console.log('frontend client says: user is already authorised!')
    var path = '/user/home'
    next({ path: path })
  } else {
    next()
  }
}

export default {
  login,
  logout,
  checkAuth,
  requireAuth,
  autoRoute
}
