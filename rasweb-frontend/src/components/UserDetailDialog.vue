<template>
  <div
    class="user-detail-dialog"
    :id="'dialog_' + dialog.username"
    @mouseleave="hideDialog()"
  >
    <v-card elevation="5" class="pa-0">
      <v-row wrap justify="center" class="pt-3">
        <v-badge bordered bottom overlap :color="dialog.online">
          <v-avatar size="45" v-if="dialog.profilePicture">
            <img :src="dialog.profilePicture" :alt="dialog.name" />
          </v-avatar>
          <v-avatar color="secondary" size="45" v-else>
            <span v-if="dialog.name" style="color: white"
              >{{ dialog.name.split(" ")[0].slice(0, 1)
              }}{{ dialog.name.split(" ")[1].slice(0, 1) }}</span
            >
            <span v-else style="color: white">{{
              dialog.username.slice(0, 2).toUpperCase()
            }}</span>
          </v-avatar>
        </v-badge>
      </v-row>
      <v-card-title class="pt-1">
        <v-row justify="center">
          {{ dialog.name }}
        </v-row>
      </v-card-title>
      <v-card-subtitle class="pt-1 pl-5 pr-0" style="margin-bottom: 0px">
        <v-icon left  color="primary">mdi-book-open-variant</v-icon>
        <span class="pt-1 pr-2">
          {{ user_detail.first_description.split("-")[0] }}
          <strong>{{ user_detail.first_description.split("-")[1] }}</strong>
        </span>
      </v-card-subtitle>
      <v-card-subtitle class="pl-5 pr-4" style="padding-top: 0px; padding-bottom: 0px">
        <v-icon left color="primary">mdi-calendar-multiple</v-icon>
        <span>{{ user_detail.second_description }}</span>
      </v-card-subtitle>
      <v-card-actions>
        <v-row justify="center" class="mt-1 mb-2">
          <v-btn @click="addChat2List({
            color: dialog.online,
            name: dialog.name,
            online: dialog.online ==='green'?true:false,
            profilePicture: dialog.profilePicture,
            username: dialog.username,
          })" small class="mr-1" color="primary">
            <v-icon left>mdi-send</v-icon>
            <span>Escríbeme</span>
          </v-btn>
          <v-btn small class="ml-1" outlined color="primary">
            <v-icon left>mdi-alert</v-icon>
            <span>Reportar</span>
          </v-btn>
        </v-row>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { mapState, mapMutations } from "vuex";

import store from "@/store/index.js";
import { setDialogPosition } from "@/auxfunctions/DomFunctions.js";
const web_domain = "http://127.0.0.1:8000";
var counter = 0;

//const web_domain = "http://127.0.0.1:8000";
export default {
  name: "UserDetailDialog",
  data: () => ({
    user_detail: {
      first_description: "",
      second_description: "",
    },
    loaded: false,
    attrs: {
      boilerplate: false,
    },
  }),
  async beforeUpdate() {
    counter++;
    if (counter > 1) {
      counter = 0;
    } else {
      let username = store.state.dialog.username;
      const api_dir = "/robotarium-api/v1.0/user-detail?username=" + username;
      let response = await fetch(web_domain + api_dir, {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
      });
      response = await response.json();
      this.user_detail.first_description = response.first_element;
      this.user_detail.second_description = response.second_element;
      setDialogPosition(username);
    }
  },
  computed: {
    ...mapState(["dialog"]),
  },
  methods: {
    hideDialog() {
      let dialog = document.getElementsByClassName("user-detail-dialog");
      dialog[0].style = "display: none;";
    },
    ...mapMutations(["addChat2List"]),
  },
};
</script>

<style>
.user-detail-dialog {
  position: fixed;
  top: 0px;
  display: none;
  transition: all ease 500ms;
}

</style>