import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    dialog : {
      name: '',
      username: '',
      profile_picture: '',
      online: '',
    },
    chat : {
      name: '',
      username: '',
      profile_picture: '',
      online: '',
      id : undefined
    }, 
    chats : []
    
  },
  mutations: {
    setAccountInfo(state,user){
      state.dialog.name = user.name;
      state.dialog.username = user.username;
      state.dialog.profile_picture = user.profile_picture;
      state.dialog.online = user.color;  
    },
    setChatInfo(state, user_params){
      let user = user_params[0]
      let index = user_params[1]
      state.chat.name = user.name;
      state.chat.username = user.username;
      state.chat.profile_picture = user.profile_picture;
      state.chat.online = user.color; 
      state.chat.id = index;
      console.log(user)
      console.log(index)
      
    },
    addChat2List(state, chat){
      state.chats.push(chat)
    }
  },
  actions: {
  },
  modules: {
  }
})
