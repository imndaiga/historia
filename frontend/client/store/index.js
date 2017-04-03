import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

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
    login: function ({ commit }, { email, password }) {
      return axios.post('/api/login', {
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'
        },
        data: {
          email: email,
          password: password
        }
      })
      .then(function (response) {
        commit('SET_USER', response.data)
      })
      .catch(function (error) {
        if (error.status === 401) {
          throw new Error('Bad credentials')
        } else {
          return error
        }
      })
    },
    logout: function ({ commit }) {
      return axios.post('/api/logout', {
        credentials: 'same-origin'
      })
      .then(function () {
        commit('SET_USER', null)
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
})

export default store
