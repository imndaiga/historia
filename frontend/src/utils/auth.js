import Auth0Lock from 'Auth0Lock'

var lockOptions = {
  auth: {
    params: {
      scope: 'openid email'
    }
  }
}

const lock = new Auth0Lock(process.env.AUTH0_ID, process.env.AUTH0_DOMAIN, lockOptions)

lock.on('authenticated', function (authResult) {
  lock.getUserInfo(authResult.accessToken, function (error, profile) {
    if (error) {
      // Handle error
      console.log('Error loading the Profile', error)
      return
    }
    localStorage.setItem('id_token', authResult.idToken)
    localStorage.setItem('profile', JSON.stringify(profile))
    location.reload()
  })
})

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
    console.log('user not authorised!')
    var path = '/'
    next({ path: path })
  } else {
    next()
  }
}

var autoRoute = function (to, from, next) {
  if (checkAuth()) {
    console.log('user is already authorised!')
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
