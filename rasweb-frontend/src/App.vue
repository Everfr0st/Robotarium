<template>
  <v-app>
    <div
      v-if="authentication.userIsAuthenticated || authentication.accessToken"
    >
      <NavBar />

      <v-main>
        <v-container fluid>
          <v-row wrap>
            <v-col class="left-aside" xs="12" sm="12" md="2" lg="1" >
              <LeftAside  />
              <v-btn class="ml-3 mt-3" small  outlined color="error darken-1" @click="Logout()"> <v-icon left>mdi-logout</v-icon> Cerrar sesión </v-btn>
            </v-col>
            <v-col 
              class="router-view"
              xs="12"
              sm="12"
              md="12"
              :lg="view == 'Robotarium' ? '10' : '9'"
              :xl="view == 'Robotarium' ? '11' : '10'"
            >
              <router-view :class="view !== 'Robotarium' ? 'view' : ''" />
            </v-col>
            <v-col
              class="right-aside"
              v-if="view !== 'Robotarium'"
              md="2"
              lg="1"
              xl="1"
            >
              <RightAside />
            </v-col>
          </v-row>
        </v-container>
      <ActiveChatList />
      </v-main>
      <UserDetailDialog />
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
    
  }),
  computed: {
    ...mapState(["authentication", "selfUser", "view", "domainBase"]),
  },
  
  methods: {
    ...mapMutations(["destroyAuthcredentials"]),
    async Logout() {
      const web_domain = "http://127.0.0.1:8000";
      const api_dir = "/robotarium-api/v1.0/logout/";
      let response = await fetch(
        web_domain + api_dir + this.authentication.accessToken,
        {
          method: "DELETE",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
          },
        }
      );

      this.destroyAuthcredentials();
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style scoped>
@media (max-width: 1264px) {
  .right-aside {
    display: none;
  }
  .left-aside {
    display: none;
  }
}
@media (min-width: 1264px) and (max-width: 1904px) {
  .left-aside {
    display: block;
  }
  .right-aside {
    display: block;
    position: relative;
  }
  .view{
    padding-right: 5%;
  }
}

.router-view{
  margin: 0 auto;
}
</style>