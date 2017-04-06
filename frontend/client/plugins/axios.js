import Vue from 'vue'
import axios from 'axios'

var HTTP = axios.create({
  // Create axios instance
  baseURL: 'http://localhost:5000'
})

Vue.prototype.$http = HTTP
