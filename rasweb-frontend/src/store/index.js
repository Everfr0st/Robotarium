import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    name: '',
    username: '',
    profile_picture: '',
    online: '',
  },
  mutations: {
    setAccountInfo(parameter){
      console.log(parameter)
    }
  },
  actions: {
  },
  modules: {
  }
})
