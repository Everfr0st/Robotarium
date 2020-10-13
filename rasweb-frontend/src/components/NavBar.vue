<template>
  <div>
    <v-app-bar app class="NavBar" dark>
      <div class="d-flex align-center">
        <v-btn :to="{ name: 'Home' }" id="logo-btn">
          <h1>LOGO</h1>
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-btn fab text>
        <v-badge
          :content="unread_messages"
          :value="unread_messages"
          color="accent"
          overlap
        >
          <v-icon> mdi-comment-text </v-icon>
        </v-badge>
      </v-btn>
      <v-btn fab text>
        <v-badge
          :content="unread_notifications"
          :value="unread_notifications"
          color="accent"
          overlap
        >
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>
      <v-btn fab text>
        <v-avatar size="30" color="blue" v-if="profile_picture">
          <img :src="profile_picture" :alt="name" />
        </v-avatar>
        <v-avatar size="30" color="secondary" v-else>
          <span>{{name.slice(0,1)}}</span>
        </v-avatar>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
const web_domain = "http://127.0.0.1:8000";
export default {
  name: "NavBar",
  data: () => ({
    unread_messages: 0,
    unread_notifications: 0,
    name: "",
    profile_picture: "",
  }),
  async created() {
    const api_dir = "/coco-api/v1.0/navbar-info";
    let nav_data = await await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    nav_data = await nav_data.json();
    this.unread_notifications = nav_data.unread_notifications;
    this.unread_messages = nav_data.unread_messages;
    this.name = nav_data.name;
    this.profile_picture = nav_data.profile_picture.length? web_domain+nav_data.profile_picture:'';
  },
  mounted() {
    const logo = document.getElementById("logo-btn");
    logo.classList.remove("v-btn--active", "v-btn--contained");
  },
  methods: {},
};
</script>

<style>
.NavBar {
  background: rgba(89, 4, 4, 1);
  background: -moz-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -webkit-gradient(
    left top,
    right top,
    color-stop(0%, rgba(89, 4, 4, 1)),
    color-stop(30%, rgba(192, 7, 7, 1)),
    color-stop(100%, rgba(192, 7, 7, 1))
  );
  background: -webkit-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -o-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -ms-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: linear-gradient(
    to right,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#590404', endColorstr='#c00707', GradientType=1 );
}
#logo-btn {
  color: white;
  background: transparent;
  border: 0px;
}
</style>