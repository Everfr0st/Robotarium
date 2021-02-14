import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import VueSSE from 'vue-sse';
import GAuth from 'vue-google-oauth2'



Vue.config.productionTip = false
Vue.use(VueSSE);

const gauthOption = {
  clientId: '923561741526-1ohpe4cr91eavr45nk68eakhq48a8tli.apps.googleusercontent.com',
  scope: 'email',
  prompt: 'select_account'
}
Vue.use(GAuth, gauthOption)

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresLogin)) {
    if (!store.getters.loggedIn) {
      next({ name: 'Login' })
    } else {
      next()
    }
  } else {
    next()
  }
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')

