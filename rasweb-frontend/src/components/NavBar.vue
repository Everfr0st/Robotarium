<template>
  <div>
    <v-app-bar id="appBar" app class="NavBar" dark>
      <v-btn
        align="left"
        color="primary"
        class="pt-2 logo-btn"
        text
        elevation="0"
        fab
        :to="{ name: 'Home' }"
      >
        <v-img
          max-height="50"
          max-width="50"
          src="@/assets/logo/LogoSir.svg"
        ></v-img>
      </v-btn>
      <a href="/"> </a>
      <v-spacer></v-spacer>

      <v-btn
        fab
        text
        @click="
          inbox = !inbox;
          notifications = false;
        "
      >
        <v-badge
          :content="unread_messages"
          :value="unread_messages"
          color="accent"
          overlap
        >
          <v-icon> mdi-comment-text-multiple </v-icon>
        </v-badge>
      </v-btn>
      <v-btn
        @click="
          notifications = !notifications;
          inbox = false;
        "
        fab
        text
      >
        <v-badge
          :content="unread_notifications"
          :value="unread_notifications"
          color="accent"
          overlap
        >
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
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
        </template>
        <v-list>
          <v-list-item class="item" :to="{ name: 'MoreInfo' }">
            <v-list-item-title>Rol</v-list-item-title>
          </v-list-item>
          <v-list-item @click="profilePicture = true;" class="item">
            <v-list-item-title >Foto de perfil</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn @click="Logout" id="logout-btn" icon>
        <v-icon>mdi-export</v-icon>
      </v-btn>
    </v-app-bar>

    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="info" v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
    <Notifications
      v-on:unreadNotifications="updateNotiStatus"
      v-if="notifications"
      class="notifications"
    />
    <Inbox
      v-if="inbox"
      style="position: fixed"
    />
    <profile-picture v-if="profilePicture" />
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import Notifications from "../components/Notifications.vue";
import Inbox from "../components/Inbox.vue";
import ProfilePicture from "../components/ProfilePicture.vue";
export default {
  name: "NavBar",
  components: {
    Notifications,
    Inbox,
    ProfilePicture
  },
  data: () => ({
    unread_messages: 0,
    unread_notifications: 0,
    name: "",
    profile_picture: "",
    username: "",
    notificationWebsocket: null,
    snackbar: false,
    message: "Tienes una nueva notificación.",
    notifications: false,
    inbox: false,
    profilePicture: false,
    apiDir: {
      logout: "/robotarium-api/v1.0/logout/",
      navBar: "/robotarium-api/v1.0/navbar-info/",
       unread: "/robotarium-api/v1.0/chat/unread-msgs"
    }
  }),
  async created() {

    let nav_data = await fetch(this.domainBase + this.apiDir.navBar, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Token ${this.authentication.accessToken}`,
      },
    });

    if (nav_data.status === 200) {
      nav_data = await nav_data.json();
      this.unread_notifications =
        nav_data.unread_notifications > 10
          ? "+10"
          : nav_data.unread_notifications;
      this.unread_messages =
        nav_data.unread_messages > 10 ? "+10" : nav_data.unread_messages;
      this.name = nav_data.name;
      this.username = nav_data.username;
      this.profile_picture = nav_data.profile_picture.length
        ? this.domainBase + nav_data.profile_picture
        : "";
      this.setSelfuser(nav_data);
      this.connect();
    } else {
      this.destroyAuthcredentials();
      this.$router.push({ name: "Login" });
    }
  },
  mounted() {
    const logo = document.getElementsByClassName("logo-btn");
    logo.forEach((boton) => {
      boton.classList.remove("v-btn--active", "v-btn--contained");
    });
    this.$root.$on("unreadMsgs", ()=>{
      this.updateCountUnreadMessages();
    })
  },
  methods: {
    ...mapMutations(["setSelfuser", "destroyAuthcredentials"]),
    async Logout() {

      let response = await fetch(
        this.domainBase + this.apiDir.logout + this.authentication.accessToken,
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
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol + this.wsBase + "/ws/notifications/" + this.username + "/"
      );
      this.websocket.onopen = () => {
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));

          const socketData = JSON.parse(data);
          if (
            socketData.type === "new_notification" &&
            socketData.sender != this.username
          ) {
            let unread_notifications =
              socketData.unread_notifications > 10
                ? "+10"
                : socketData.unread_notifications;
            this.unread_notifications = unread_notifications;
            this.snackbar = true;
          } else if(socketData.type === "new_msg" && socketData.sender != this.username){
            this.updateCountUnreadMessages();
          }
        };
      };
      this.websocket.onclose = () => {};
    },
    updateNotiStatus(unread_notifications) {
      this.unread_notifications = unread_notifications;
    },
    updateMsgStatus(unreadMessages) {
      this.unread_messages = unreadMessages;
    },
    updateCountUnreadMessages(){
      fetch(this.domainBase + this.apiDir.unread, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.unread_messages = response.unread_messages > 10?'+10':response.unread_messages;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    
  },
  computed: {
    ...mapState(["authentication", "wsBase", "domainBase"]),
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
.logo-btn {
  color: white;
  background: transparent;
  border: 0px;
}
@media (max-width: 1264px) {
  #logout-btn {
    display: block;
  }
}
@media (min-width: 1264px) {
  #logout-btn {
    display: none;
  }
}
.item:hover{
  background: rgb(241, 241, 241);
  cursor: pointer;
}
</style>