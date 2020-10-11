<template>
  <div class="user-detail-dialog">
    <v-container>
      <v-row wrap>
        <v-badge bordered bottom :color="online">
          <v-avatar size="45" v-if="profile_picture">
            <img :src="profile_picture" :alt="name" />
          </v-avatar>
          <v-avatar color="secondary" size="45" v-else>
            <span>
              {{ name_init }}
            </span>
          </v-avatar>
        </v-badge>
      </v-row>
      <v-row>
        <h3>{{ name }}</h3>
      </v-row>
     
    </v-container>
  </div>
</template>
<script>
const web_domain = "http://127.0.0.1:8000";

import { mapState } from 'vuex'

export default {
  name: "UserDetailDialog",
  data: () => ({
    
    user_detail: undefined,
    loaded: false,
    attrs: {
      boilerplate: false,
    },
  }),
  /*async created() {
    const api_dir = "/coco-api/v1.0/users-list";
    let response = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    //Just have to get Role, carreer, semester or department and date begun to work
  },*/
  computed:{
      ...mapState(["name", "username", "profile_picture", "online"])
  }
};
</script>