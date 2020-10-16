import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta : {
      requiresLogin : true
    }
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: () => import('../views/Inventory.vue'),
    meta : {
      requiresLogin : true
    }
  },
  {
    path: '/robotarium',
    name: 'Robotarium',
    component: () => import('../views/Robotarium.vue'),
    meta : {
      requiresLogin : true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
