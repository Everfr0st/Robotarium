import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: localStorage.getItem("token"),
      refreshToken: localStorage.getItem("refresh_token"),
      userIsAuthenticated: !!localStorage.getItem("token"),
    },
    selfUser: {
      username: '',
      profile_picture: '',
      name: '',
    },
    dialog: {
      name: '',
      username: '',
      profilePicture: '',
      online: '',
    },
    live:{
      timeElapsed: '',
      started: false,
      finished: false,
    },
    robotarium:'',
    chats: [],
    users: [],
    wsBase : '127.0.0.1:8000',
    domainBase : 'http://127.0.0.1:8000',
    view: '',


  },
  mutations: {
    updateAuthcredentials(state, { access, refresh, auth }) {
      state.authentication.accessToken = access;
      state.authentication.refreshToken = refresh;
      state.authentication.userIsAuthenticated = auth;
      localStorage.setItem('refresh_token', state.authentication.refreshToken)
      localStorage.setItem('token', state.authentication.accessToken)
    },
    destroyAuthcredentials(state){
      state.authentication.accessToken = null;
      state.authentication.refreshToken = null;
      state.authentication.userIsAuthenticated = false;
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
    },
    setSelfuser(state, user) {
      state.selfUser.username = user.username;
      state.selfUser.profilePicture = user.profilePicture? state.domainBase + user.profilePicture: "";
      state.selfUser.name = user.name;
    },
    setAccountInfo(state, user) {
      state.dialog.name = user.name;
      state.dialog.username = user.username;
      state.dialog.profilePicture = user.profilePicture;
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
    updateLiveObj(state, liveObj){
      
      state.live = liveObj
    },
    setViewname(state, view){
      state.view = view;
    },
    setRobotariumInfo(state,robotariumInfo){
      state.robotarium = robotariumInfo;
    }
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

