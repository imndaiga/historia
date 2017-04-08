import Vue from 'vue'

function logout () {
  if (process.browser) {
    localStorage.removeItem('id_token')
    localStorage.removeItem('user')
    Vue.prototype.$http.defaults.headers.common['Authorization'] = 'Bearer ' + null
  }
}

Vue.prototype.logout = logout
