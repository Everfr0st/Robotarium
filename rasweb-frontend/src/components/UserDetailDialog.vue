<template>
  <div
    class="user-detail-dialog"
    :id="'dialog_' + dialog.username"
    @mouseleave="hideDialog()"
  >
    <v-card elevation="5">
      <v-row wrap justify="center" class="pa-3">
        <v-badge
          bordered
          bottom
          overlap
          :color="dialog.online ? 'green' : 'grey'"
        >
          <v-avatar size="45" v-if="dialog.profile_picture">
            <img :src="dialog.profile_picture" :alt="dialog.name" />
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
      <v-card-title justify="center" class="mt-1 dialog-name">
        {{ dialog.name }}
      </v-card-title>
      <v-card-subtitle class="pt-1 pl-5 pr-0" style="margin-bottom: 0px">
        <v-icon left color="primary">mdi-book-open-variant</v-icon>
        <span class="pt-1 pr-2">
          {{ user_detail.first_description.split("-")[0] }}
          <strong>{{ user_detail.first_description.split("-")[1] }}</strong>
        </span>
      </v-card-subtitle>
      <v-card-subtitle
        class="pl-5 pr-4"
        style="padding-top: 0px; padding-bottom: 0px"
      >
        <v-icon left color="primary">mdi-calendar-multiple</v-icon>
        <span>{{ user_detail.second_description }}</span>
      </v-card-subtitle>
      <v-card-actions>
        <v-row justify="center" class="mt-1 mb-2 px-5">
          <v-btn
            @click="
              addChat2List({
                username: dialog.username,
                name: dialog.name,
                online: dialog.online,
                profile_picture: dialog.profilePicture,
              })
            "
            small
            class="mr-1"
            color="primary"
          >
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

import { setDialogPosition } from "@/auxfunctions/DomFunctions.js";

export default {
  name: "UserDetailDialog",
  data: () => ({
    user_detail: {
      first_description: "",
      second_description: "",
    },
    apiDir: "/robotarium-api/v1.0/user-detail?username=",
    loaded: false,
    attrs: {
      boilerplate: false,
    },
  }),
  beforeUpdate(){
    this.getUserData();
  },
  mounted() {
    this.getUserData();
  },
  computed: {
    ...mapState(["dialog", "domainBase"]),
  },

  methods: {
    ...mapMutations(["addChat2List"]),
    hideDialog() {
      this.$root.$emit("detailDialog", false);
    },
    async getUserData() {
      let username = this.dialog.username;
      setDialogPosition(username);
      fetch(this.domainBase + this.apiDir + username, {
        method: "GET",
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.user_detail.first_description = response.first_element;
          this.user_detail.second_description = response.second_element;
        });
    },
  },
};
</script>

<style>
.user-detail-dialog {
  position: fixed;
  transition: all ease 500ms;
  z-index: 10;
}
.dialog-name {
  text-align: center;
}
</style>