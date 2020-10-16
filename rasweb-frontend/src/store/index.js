import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: localStorage.getItem("token"),
      refreshToken: null,
      user_is_authenticated: false,
    },
    self_user: '',
    dialog: {
      name: '',
      username: '',
      profile_picture: '',
      online: '',
    },
    chats: []

  },
  mutations: {
    updateAuthcredentials(state, { access, refresh, auth }) {
      state.authentication.accessToken = access;
      state.authentication.refreshToken = refresh;
      state.authentication.user_is_authenticated = auth;
      localStorage.setItem('token', state.authentication.accessToken)
    },
    destroyAuthcredentials(state){
      state.authentication.accessToken = null;
      state.authentication.refreshToken = null;
      state.authentication.user_is_authenticated = false;
      localStorage.removeItem('token');
    },
    setSelfuser(state, username) {
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
    },
    deleteChatfromlist(state, chat) {
      let chat_in_list = state.chats.indexOf(chat)
      if (chat_in_list != -1) {
        state.chats.splice(chat_in_list, 1);
      }
    },
  },
  actions: {
 
  },
  modules: {
  },
  getters:{
    loggedIn(state){
      return state.authentication.accessToken != null
    }
  }
})

