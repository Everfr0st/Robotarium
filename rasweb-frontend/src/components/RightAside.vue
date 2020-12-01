<template >
  <div class="ma-0 pa-0 users-list">
    <v-container class="pa-0">
      <v-row class="ml-8">
        <v-text-field
          class="search-user"
          v-model="search"
          append-icon="mdi-account-search"
          label="Buscar"
          single-line
          hide-details
          @keyup="searchUser()"
        ></v-text-field>
      </v-row>
      <div v-if="loaded" id="chat-list" @mouseleave="hideDialog()">
        <v-list style="margin-left: 20px; width: 90%" two-line>
          <template v-for="(user, index) in users">
            <v-list-item
              :key="index"
              class="user-list"
              :id="'user_' + user.username"
              @mouseenter="
                setAccountInfo(user);
                showDialog();
              "
              @click="addChat2List(user)"
            >
              <v-badge
                bordered
                bottom
                :color="user.color"
                offset-x="25px"
                offset-y="25px"
                dot
              >
                <v-list-item-avatar v-if="user.profile_picture.length">
                  <v-img :src="user.profile_picture"></v-img>
                </v-list-item-avatar>
                <v-list-item-avatar v-else color="primary">
                  <span v-if="user.name" style="color: white"
                    >{{ user.name.split(" ")[0].slice(0, 1)
                    }}{{ user.name.split(" ")[1].slice(0, 1) }}</span
                  >
                  <span v-else style="color: white">{{
                    user.username.slice(0, 2).toUpperCase()
                  }}</span>
                </v-list-item-avatar>
              </v-badge>

              <v-list-item-content>
                <v-list-item-title v-html="user.name"></v-list-item-title>
                <v-list-item-subtitle
                  v-html="'@' + user.username"
                ></v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </div>
      <div v-else class="ml-3">
        <v-skeleton-loader
          v-for="index in 7"
          :key="index"
          v-bind="attrs"
          type="list-item-avatar-two-line"
        ></v-skeleton-loader>
      </div>
    </v-container>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { setDialogPosition } from "@/auxfunctions/DomFunctions.js";


export default {
  name: "RightAside",
  data: () => ({
    loaded: false,
    search: "",
     api_dir: "/robotarium-api/v1.0/users-list",
    attrs: {
      boilerplate: false,
    },
  }),
  computed: {
    ...mapState(["users", "authentication", "dialog", "domainBase"]),
  },
  methods: {
    ...mapMutations([
      "setUsers",
      "setAccountInfo",
      "setChatInfo",
      "addChat2List",
    ]),
    hideDialog() {
      let chatlist = document.getElementById("chat-list");
      let chatlist_position = chatlist.getBoundingClientRect();
      let dialog = document.getElementsByClassName("user-detail-dialog");
      if (
        event.clientY > chatlist_position.bottom ||
        event.clientY < chatlist_position.top
      ) {
        dialog[0].style = "display: none;";
      }
    },
    showDialog() {
      let username = this.dialog.username;
      let dialogdiv = document.getElementsByClassName("user-detail-dialog");
     // setDialogPosition(username);
    },
    searchUser() {
        let usersList = document.getElementsByClassName("v-list-item__title");
        let userslistContainers = document.getElementsByClassName("user-list");
        for (var i = 0; i < usersList.length; i++) {
          var txtValue = usersList[i].textContent || usersList[i].innerText;
          if (txtValue.toUpperCase().indexOf(this.search.toUpperCase()) > -1) {
            userslistContainers[i].style.display = "";
          } else {
            userslistContainers[i].style.display = "none";
          }
        }
      
    },
  },
  async created() {
    let response = await fetch(this.domainBase + this.api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Bearer ${this.authentication.accessToken}`,
      },
    });
    response = await response.json();
    this.setUsers(response);
    this.loaded = true;
  },
};
</script>

<style scoped>
.btn-menu {
  background-color: rgba(190, 7, 7, 0.4);
}
.user-list {
  padding: 0px;
}
.user-list:hover {
  border-radius: 5px;
  background-color: #e7e7e7;
  cursor: pointer;
}
.users-list {
  position: fixed;
  right: 0px;
  top: 12%;
  width: 23%;
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
}
.users-list::-webkit-scrollbar {
  width: 5px; /* Tamaño del scroll en vertical */
  height: 5px; /* Tamaño del scroll en horizontal */
  /* display: none; Ocultar scroll */
}
/* Ponemos un color de fondo y redondeamos las esquinas del thumb */
.users-list::-webkit-scrollbar-thumb {
  background: #be0707;
  border-radius: 4px;
}
.search-user {
  max-width: 87%;
  background: white;
}
</style>