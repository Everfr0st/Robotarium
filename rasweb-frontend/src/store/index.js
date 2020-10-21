import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: localStorage.getItem("token"),
      refreshToken: localStorage.getItem("refresh_token"),
      user_is_authenticated: !!localStorage.getItem("token"),
    },
    self_user: {
      username: '',
      profile_picture: '',
      name: '',
    },
    dialog: {
      name: '',
      username: '',
      profile_picture: '',
      online: '',
    },
    chats: [],
    users: [],
    ws_base : '127.0.0.1:8000',
    domain_base : 'http://127.0.0.1:8000'

  },
  mutations: {
    updateAuthcredentials(state, { access, refresh, auth }) {
      state.authentication.accessToken = access;
      state.authentication.refreshToken = refresh;
      state.authentication.user_is_authenticated = auth;
      localStorage.setItem('refresh_token', state.authentication.refreshToken)
      localStorage.setItem('token', state.authentication.accessToken)
    },
    destroyAuthcredentials(state){
      state.authentication.accessToken = null;
      state.authentication.refreshToken = null;
      state.authentication.user_is_authenticated = false;
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
    },
    setSelfuser(state, user) {
      state.self_user.username = user.username;
      state.self_user.profile_picture = state.domain_base + user.profile_picture;
      state.self_user.name = user.name;
    },
    setAccountInfo(state, user) {
      state.dialog.name = user.name;
      state.dialog.username = user.username;
      state.dialog.profile_picture = user.profile_picture;
      state.dialog.online = user.color;
    },
    setUsers(state, users){
      state.users = users;
    },
    addChat2List(state, chat) {
      let chat_in_list = state.chats.indexOf(chat)
      if (chat_in_list === -1) {
        state.chats.push(chat)
      }
    },
    deleteChatfromlist(state, index) {
      state.chats.splice(index, 1);
    
      //this.$delete(this.chats, index);

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

