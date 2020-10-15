import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    self_user:'',
    dialog: {
      name: '',
      username: '',
      profile_picture: '',
      online: '',
    },
    chats: []

  },
  mutations: {
    setSelfuser(state,username){
      state.self_user = username;
    },
    setAccountInfo(state, user) {
      state.dialog.name = user.name;
      state.dialog.username = user.username;
      state.dialog.profile_picture = user.profile_picture;
      state.dialog.online = user.color;
    },
    addChat2List(state, chat) {
      let chat_in_list = state.chats.indexOf(chat)
      if (chat_in_list === -1) {
        state.chats.push(chat)
      }
      console.log(chat_in_list)
    },
    deleteChatfromlist(state, chat){
      let chat_in_list = state.chats.indexOf(chat)
      console.log(chat,chat_in_list)
      if (chat_in_list != -1) {
        state.chats.splice(chat_in_list, 1);
      }
    }
  },
  actions: {
  },
  modules: {
  }
})

