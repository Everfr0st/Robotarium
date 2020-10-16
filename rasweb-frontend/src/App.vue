<template>
  <v-app>
    <div v-if="authentication.user_is_authenticated || authentication.accessToken">
    
    <NavBar />
    <v-main>
      <v-container fluid>
        <v-row wrap>
          <v-col sm="12" md="3" lg="3" color="primary">
            <LeftAside />
          </v-col>
          <v-col sm="12" md="6" color="red">
            <router-view />
          </v-col>
          <v-col class="user-list" sm="12" md="3" lg="3">
            <RightAside />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-btn color="error" @click="Logout()">
      Cerrar sesión
    </v-btn>
    <UserDetailDialog />
    <ActiveChatList />
    </div>

    <div v-else>
      <router-view />
    </div>
  </v-app>
</template>

<script>
import LeftAside from "@/components/LeftAside.vue";
import RightAside from "@/components/RightAside.vue";
import NavBar from "@/components/NavBar.vue";
import UserDetailDialog from "@/components/UserDetailDialog.vue";
import ActiveChatList from "@/components/ActiveChatList.vue";

import {mapState, mapMutations} from "vuex";

export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    RightAside,
    UserDetailDialog,
    ActiveChatList,
  },

  data: () => ({
    //
  }),
  computed:{
    ...mapState(["authentication"])
  },
  methods: {
    ...mapMutations(["destroyAuthcredentials"]),
    Logout(){
      localStorage.removeItem("token");
      this.destroyAuthcredentials()
      this.$router.push({name: 'Login'})
      
    }
  }
};
</script>

<style scoped>
.user-list {
  max-height: 85vh;
  height: 85vh;
  border-left: 1px solid #e7e7e7;
  padding: 0px;
  margin: 0px;
  overflow-y: auto;
  overflow-x: hidden;
}
.user-list::-webkit-scrollbar {
  width: 3px; /* Tamaño del scroll en vertical */
  height: 3px; /* Tamaño del scroll en horizontal */
  /* display: none; Ocultar scroll */
}
/* Ponemos un color de fondo y redondeamos las esquinas del thumb */
.user-list::-webkit-scrollbar-thumb {
  background: #be0707;
  border-radius: 4px;
}
</style>