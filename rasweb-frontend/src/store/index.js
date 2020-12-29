import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: localStorage.getItem("token"),
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
    reservation:'',
    robotarium:'',
    chats: [],
    users: [],
    wsBase : '127.0.0.1:8000',
    domainBase : 'http://127.0.0.1:8000',
    view: '',
  },
  mutations: {
    updateAuthcredentials(state, { access, auth }) {
      state.authentication.accessToken = access;
      state.authentication.userIsAuthenticated = auth;
      localStorage.setItem('token', access)
    },
    destroyAuthcredentials(state){
      state.authentication.accessToken = null;
      state.authentication.userIsAuthenticated = false;
      localStorage.removeItem('token');
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
      state.dialog.online = user.online;
    },
    setUsers(state, users){
      state.users = users;
    },
    addChat2List(state, chat) {
      let auxChat = {
        username: chat.username,
        name: chat.name,
        online: chat.online,
        profile_picture: chat.profile_picture
      }
      let chat_in_list = state.chats.indexOf(auxChat)
      console.log(auxChat, state.chats)
      if (chat_in_list==-1) {
        state.chats.push(auxChat)
      }
    },
    deleteChatfromlist(state, index) {
      state.chats.splice(index, 1);
      console.log(state.chats)
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
    },
    setReservation(state,reservation){
      state.reservation = reservation;
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

