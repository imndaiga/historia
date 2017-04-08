import Vue from 'vue'
import axios from 'axios'

const server = axios.create()

function login (loginData) {
  return server.post('/auth/login', {
    headers: {
      'Content-Type': 'application/json'
    },
    email: loginData.email,
    password: loginData.password
  })
  .then(function (response) {
    if (process.browser) {
      localStorage.setItem('id_token', response.data.token)
      localStorage.setItem('user', response.data.user)
      Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('id_token')
    }
    return response
  })
  .catch(function (error) {
    return error
  })
}

Vue.prototype.login = login
