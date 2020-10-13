<template>
  <div class="ma-0 pa-0">
    <v-divider vertical></v-divider>
    <v-container class="pa-0">
      <v-row class="ml-8">
        <h3 style="padding-top: 5px" align-center>Usuarios</h3>
        <v-spacer></v-spacer>
        <v-btn fab text small color="grey" class="mr-6">
          <v-icon>mdi-home</v-icon>
        </v-btn>
      </v-row>

      <v-list  v-if="loaded" two-line>
      
        <template  v-for="(user, index) in users">
          <v-list-item :key="index" class="user-list" 
          @click="setAccountInfo(user)">
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
                <span v-if="user.name" style="color: white">{{user.name.split(" ")[0].slice(0,1)}}{{user.name.split(" ")[1].slice(0,1)}}</span>
                <span v-else style="color: white">{{user.username.slice(0,2).toUpperCase()}}</span>
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

import { mapMutations } from 'vuex';

const web_domain = "http://127.0.0.1:8000";

export default {
  name: "RightAside",
  data: () => ({
    users: [],
    loaded: false,
    attrs: {
      boilerplate: false,
    },
  }),
  methods: {
    ...mapMutations(["setAccountInfo"])
  },
  async created() {
    const api_dir = "/coco-api/v1.0/users-list";
    let response = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    response = await response.json();
    this.users = response;
    this.loaded = true;
  },
 
  
};
</script>

<style scoped>
.btn-menu {
  background-color: rgba(190, 7, 7, 0.4);
}

.user-list:hover {
  border-radius: 5px;
  background-color:#E7E7E7;
  cursor: pointer;
  
}
</style>