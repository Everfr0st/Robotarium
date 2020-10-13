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
    setAccountInfo(state,parameter){
      state.name = parameter.name;
      state.username = parameter.username;
      state.profile_picture = parameter.profile_picture;
      state.online = parameter.color;
    }
  },
  actions: {
  },
  modules: {
  }
})
