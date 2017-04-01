import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

require('whatwg-fetch')

const store = new Vuex.Store({
  state: {
    authUser: null
  },
  mutations: {
    SET_USER: function (state, user) {
      state.authUser = user
    }
  },
  actions: {
    nuxtServerInit: function ({ commit }, { req }) {
      if (req.session && req.session.authUser) {
        commit('SET_USER', req.session.authUser)
      }
    },
    login: function ({ commit }, { username, password }) {
      return fetch('api/login', {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username,
          password
        })
      })
      .then(function (res) {
        if (res.status === 401) {
          throw new Error('Bad credentials')
        } else {
          return res.json()
        }
      })
      .then(function (authUser) {
        commit('SET_USER', authUser)
      })
    },
    logout: function ({ commit }) {
      return fetch('/api/logout', {
        credentials: 'same-origin',
        method: 'POST'
      })
      .then(function () {
        commit('SET_USER', null)
      })
    }
  }
})

export default store
