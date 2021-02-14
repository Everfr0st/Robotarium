<template>
  <v-app>
    <div
      v-if="authentication.userIsAuthenticated || authentication.accessToken"
    >
      <NavBar />

      <v-main id="main">
        <v-btn
          @click="toggleMenu"
          color="white secondary--text"
          id="show-left-aside"
          v-if="view == 'Robotarium'"
        >
          <v-icon> {{ menuOpen ? "mdi-menu-open" : "mdi-menu" }} </v-icon>
          <span class="ml-2" v-if="!menuOpen">Menú</span>
        </v-btn>
        <v-container fluid>
          <v-row wrap>
            <v-col
              :class="view !== 'Robotarium' ? '' : 'menu-robotarium'"
              id="left-aside"
              xs="12"
              sm="12"
              md="2"
              lg="1"
            >
              <LeftAside />
              <v-btn
                class="ml-4 mt-5"
                small
                outlined
                color="error darken-1"
                @click="Logout()"
              >
                <v-icon left>mdi-logout</v-icon>
                <span class="logout">Cerrar sesión</span></v-btn
              >
            </v-col>
            <v-col
              class="router-view"
              xs="12"
              sm="12"
              md="12"
              :lg="view == 'Robotarium' ? '12' : '9'"
              :xl="view == 'Robotarium' ? '12' : '10'"
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
      <UserDetailDialog v-if="detailDialog && view != 'Robotarium'" />
    </div>

    <div v-else>
      <router-view />
    </div>
    <BottomNavBar />
  </v-app>
</template>

<script>
import LeftAside from "@/components/LeftAside.vue";
import RightAside from "@/components/RightAside.vue";
import NavBar from "@/components/NavBar.vue";
import UserDetailDialog from "@/components/UserDetailDialog.vue";
import ActiveChatList from "@/components/ActiveChatList.vue";
import BottomNavBar from "@/components/BottomNavBar.vue";

import { mapState, mapMutations } from "vuex";

export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    RightAside,
    UserDetailDialog,
    ActiveChatList,
    BottomNavBar,
  },

  data: () => ({
    menuOpen: false,
    apiDir: "/robotarium-api/v1.0/logout/",
    detailDialog: false,
  }),
  computed: {
    ...mapState(["authentication", "selfUser", "view", "domainBase", "dialog"]),
  },
  mounted() {
    this.$root.$on("detailDialog", (status) => {
      this.detailDialog = status;
      console.log(status, "detail");
    });
  },
  watch:{
    view(){
      this.menuOpen = false;
    }
  },
  methods: {
    ...mapMutations(["destroyAuthcredentials"]),
    async Logout() {
      let response = await fetch(this.domainBase + this.apiDir, {
        method: "DELETE",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      });

      this.destroyAuthcredentials();
      this.$router.push({ name: "Login" });
    },
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
      var menu = document.getElementById("left-aside");
      var menuBtn = document.getElementById("show-left-aside");
      if (this.menuOpen) {
        menu.classList.add("menu-robotarium-active");
        menuBtn.classList.add("active");
      } else {
        menu.classList.remove("menu-robotarium-active");
        menuBtn.classList.remove("active");
      }
    },
  },
};
</script>

<style scoped>
@media (max-width: 1200px) {
  .right-aside {
    display: none;
  }
  #left-aside {
    display: none;
  }
  #main {
    padding: 50px 0 !important;
  }
  .menu-robotarium {
    display: none;
  }
  #show-left-aside {
    display: none;
  }
}
@media (min-width: 1264px) and (max-width: 1904px) {
  #left-aside {
    display: block;
  }
  .right-aside {
    display: block;
    position: relative;
  }
  .view {
    padding-right: 5%;
  }
}

.router-view {
  margin: 0 auto;
}
.logout {
  font-size: 7pt;
}
.menu-robotarium {
  position: fixed;
  left: -400px;
  top: 65px;
  z-index: 100;
  min-width: 200px;
  max-width: 400px;
  width: auto;
  background: white;
  height: 100vh;
  transition: all ease 500ms;
  -webkit-box-shadow: 0px 3px 33px -12px rgba(0, 0, 0, 0.76);
  -moz-box-shadow: 0px 3px 33px -12px rgba(0, 0, 0, 0.76);
  box-shadow: 0px 3px 33px -12px rgba(0, 0, 0, 0.76);
}
.menu-robotarium-active {
  left: 0px;
}
#show-left-aside {
  position: fixed;
  left: 0px;
  top: 65px;
  z-index: 1000;

  transition: all ease 600ms;
}
#show-left-aside.active {
  left: 200px;
  -webkit-box-shadow: 3px 3px 3px 1px rgba(92, 92, 92, 0.29);
  -moz-box-shadow: 3px 3px 3px 1px rgba(92, 92, 92, 0.29);
  box-shadow: 3px 3px 3px 1px rgba(92, 92, 92, 0.29);
  border-radius: 0% 3px 3px 0;
}
</style>