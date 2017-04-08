import Vue from 'vue'
import axios from 'axios'

var HTTP = axios.create({
  // Create axios instance
  baseURL: process.env.backendUrl
})

Vue.prototype.$http = HTTP

if (process.browser) {
  var BearerAuth = localStorage ? 'Bearer ' + localStorage.getItem('id_token') : 'Bearer ' + null
  Vue.prototype.$http.defaults.headers.common['Authorization'] = BearerAuth
}
