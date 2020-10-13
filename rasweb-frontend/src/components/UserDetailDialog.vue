<template>
  <div class="user-detail-dialog">
    <v-container>
      <v-row wrap class="mb-2">
        <v-badge bordered bottom overlap :color="online">
          <v-avatar size="45" v-if="profile_picture">
            <img :src="profile_picture" :alt="name" />
          </v-avatar>
          <v-avatar color="secondary" size="45" v-else>
            <span v-if="name" style="color: white">{{name.split(" ")[0].slice(0,1)}}{{name.split(" ")[1].slice(0,1)}}</span>
                <span v-else style="color: white">{{username.slice(0,2).toUpperCase()}}</span>
          </v-avatar>
        </v-badge>
      </v-row>
      <v-row>
        <h3>{{ name }}</h3>
        
      </v-row>
      <v-row>
        <p>@{{ username}}</p>
        
      </v-row>
      <v-row>
        <v-icon> mdi-book-open </v-icon>
        <p>{{user_detail.first_description.split("-")[0]}} <strong>{{user_detail.first_description.split("-")[1]}}</strong> </p>
        
      </v-row>
      <v-row>
        <v-icon> mdi-clock </v-icon>
        <p>{{user_detail.second_description}}</p>
        
      </v-row>
      <v-row>
        <v-btn color="primary">
          <v-icon>mdi-send</v-icon>
          <p>Escríbeme</p>
        </v-btn>
        <v-btn outlined color="primary">
          <v-icon>mdi-report</v-icon>
          <p>Reportar</p>
        </v-btn>
      </v-row>
     
    </v-container>
  </div>
</template>
<script>

import { mapState } from 'vuex'
import store from '@/store/index.js';

const web_domain = "http://127.0.0.1:8000";

//const web_domain = "http://127.0.0.1:8000";
export default {
  name: "UserDetailDialog",
  data: () => ({
    
    user_detail: {
      first_description : '',
      second_description : ''
    },
    loaded: false,
    attrs: {
      boilerplate: false,
    },
  }),
  async updated(){
    const api_dir = "/coco-api/v1.0/user-detail?username=" + store.state.username;
    let response = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    response = await response.json();
    this.user_detail.first_description = response.first_element;
    this.user_detail.second_description = response.second_element;
    console.log(response)
  },
  computed:{
      ...mapState(["name", "username", "profile_picture", "online"])
  },
  
};
</script>