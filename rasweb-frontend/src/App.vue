<template>
  <v-app style="min-width: 800px;">
    
    <div
      v-if="authentication.userIsAuthenticated || authentication.accessToken"
    >
      <NavBar />
     
      <v-main>
        <v-container fluid>
          <v-row wrap>
            <v-col sm="12" md="3" lg="2">
              <LeftAside />   
            </v-col>
            <v-col sm="12" md="9" :lg="view =='Robotarium'?'10':'7'">
              <router-view />
            </v-col>
            <v-col v-if="view !=='Robotarium'" class="user-container-list">
              <RightAside />
            </v-col>
          </v-row>
        </v-container>
      </v-main>
      <v-btn color="error" @click="Logout()"> Cerrar sesión </v-btn>
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

import { mapState, mapMutations } from "vuex";

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
  computed: {
    ...mapState(["authentication", "selfUser", "view"]),
  },
  methods: {
    ...mapMutations(["destroyAuthcredentials"]),
    async Logout() {
      const web_domain = "http://127.0.0.1:8000";
      const api_dir = "/robotarium-api/v1.0/logout/";
      let response = await fetch(web_domain + api_dir + this.authentication.accessToken, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${this.authentication.accessToken}`,
        },
      });

      this.destroyAuthcredentials();
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style scoped>
.user-container-list {
  position: fixed;
  right: 0px;
  top: 12%;
  width: 22%;
  max-height: 85vh;
  height: 85vh;
  padding: 0px;
  margin: 0px;
  overflow-y: auto;
  overflow-x: hidden;
}
.user-container-list::-webkit-scrollbar {
  width: 3px; /* Tamaño del scroll en vertical */
  height: 3px; /* Tamaño del scroll en horizontal */
  /* display: none; Ocultar scroll */
}
/* Ponemos un color de fondo y redondeamos las esquinas del thumb */
.user-container-list::-webkit-scrollbar-thumb {
  background: #be0707;
  border-radius: 4px;
}
</style>