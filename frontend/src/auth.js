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

export default {
  login,
  logout
}
