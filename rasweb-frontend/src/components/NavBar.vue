<template>
  <div>
    <v-app-bar app class="NavBar" dark>
      <v-btn
      align="left"
          color="primary"
          class="pt-2"
          text
          elevation="0"
          fab
      :to="{ name: 'Home' }" id="logo-btn"
    >
      <v-img
              max-height="50"
              max-width="50"
              src="@/assets/logo/LogoSir.svg"
            ></v-img>
    </v-btn>
      <a href="/">
        
      </a>
      <v-spacer></v-spacer>

      <v-btn fab text>
        <v-badge
          :content="unread_messages"
          :value="unread_messages"
          color="accent"
          overlap
        >
          <v-icon> mdi-comment-text-multiple </v-icon>
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
          <span style="color: white">{{
            name.trim().length
              ? name.slice(0, 1) + name.split(" ")[1].slice(0, 1)
              : username.slice(0, 1)
          }}</span>
        </v-avatar>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  name: "NavBar",
  data: () => ({
    unread_messages: 0,
    unread_notifications: 0,
    name: "",
    profile_picture: "",
    username: "",
  }),
  async created() {
    const web_domain = "http://127.0.0.1:8000";
    const api_dir = "/robotarium-api/v1.0/navbar-info/";
    let nav_data = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Bearer ${this.authentication.accessToken}`,
      },
    });

    if (nav_data.status === 200) {
      nav_data = await nav_data.json();
      this.unread_notifications = nav_data.unread_notifications;
      this.unread_messages = nav_data.unread_messages;
      this.name = nav_data.name;
      this.username = nav_data.username;
      this.profile_picture = nav_data.profile_picture.length
        ? web_domain + nav_data.profile_picture
        : "";
      this.setSelfuser(nav_data);
    } else {
      this.destroyAuthcredentials();
      this.$router.push({ name: "Login" });
    }
  },
  mounted() {
    const logo = document.getElementById("logo-btn");
    logo.classList.remove("v-btn--active", "v-btn--contained");
  },
  methods: {
    ...mapMutations(["setSelfuser", "destroyAuthcredentials"]),
  },
  computed: {
    ...mapState(["authentication"]),
  },
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