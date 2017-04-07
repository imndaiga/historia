import Vue from 'vue'
import axios from 'axios'

var HTTP = axios.create({
  // Create axios instance
  baseURL: process.env.backendUrl
})

Vue.prototype.$http = HTTP
