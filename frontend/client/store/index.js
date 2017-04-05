import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

var server = axios.create()

const store = new Vuex.Store({
  state: {
    authUser: null,
    alert: {
      message: '',
      type: '',
      duration: 0,
      dismissable: true
    }
  },
  mutations: {
    SET_USER: function (state, user) {
      state.authUser = user
    },
    SET_ALERT: function (state, alertObject) {
      state.alert = alertObject
    }
  },
  actions: {
    nuxtServerInit: function ({ commit }, { req }) {
      if (req.session && req.session.authUser) {
        commit('SET_USER', req.session.authUser)
      }
    },
    login: function ({ commit }, { email, password }) {
      return server.post('/auth/login', {
        headers: {
          'Content-Type': 'application/json'
        },
        email: email,
        password: password
      })
      .then(function (response) {
        commit('SET_USER', response.data)
        return response
      })
      .catch(function (error) {
        return error
      })
    },
    logout: function ({ commit }) {
      return server.post('/auth/logout')
      .then(function () {
        commit('SET_USER', null)
      })
    },
    alert: function ({ commit }, { message, type, duration, dismissable }) {
      return commit('SET_ALERT', {
        message: message,
        type: type,
        duration: duration,
        dismissable: dismissable
      })
    },
    dismiss_alert: function ({ commit }) {
      return commit('SET_ALERT', {
        message: '',
        type: '',
        duration: 0,
        dismissable: true
      })
    }
  }
})

export default store
