import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    modalIsOpen: false
  },
  mutations: {
    toggleModal: function (state) {
      state.modalIsOpen = !state.modalIsOpen
    }
  },
  actions: {
    openModal: function ({ commit }) {
      commit('toggleModal')
    },
    closeModal: function ({ commit }) {
      commit('toggleModal')
    }
  }
})
