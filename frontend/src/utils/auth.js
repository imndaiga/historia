import Auth0Lock from 'Auth0Lock'

var lockOptions = {
  auth: {
    params: {
      scope: 'email'
    }
  }
}

const lock = new Auth0Lock(process.env.AUTH0_ID, process.env.AUTH0_DOMAIN, lockOptions)

lock.on('authenticated', function (authResult) {
  localStorage.setItem('id_token', authResult.idToken)

  lock.getUserInfo(authResult.accessToken, function (error, profile) {
    if (error) {
      // Handle error
      console.log('Error loading the Profile', error)
    } else {
      // Set the token and user profile in local storage
      localStorage.setItem('profile', JSON.stringify(profile))
    }
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

export default {
  login,
  logout,
  checkAuth,
  requireAuth
}
