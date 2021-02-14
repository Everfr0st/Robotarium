<template>
  <v-card elevation="5" class="noti-card px-0" width="300" max-width="300">
    <v-card-title class="pa-0 ml-3 mt-3"> Notificaciones </v-card-title>
     <v-card-subtitle class="mt-2 " v-if="!notifications.length">Aún no tienes notificaciones  😕 </v-card-subtitle>
    <v-card-text class="pa-0 ma-0">
     
      <v-list-item
        three-line
        v-for="(notification, index) in notifications"
        :key="index"
        :class="notification.read?'notification': 'notification noti-unread'"
      >
        <v-badge
          offset-x="30px"
          offset-y="30px"
          bottom
          overlap
          color="accent"
          :icon="getIcon(notification.type)"
        >
          <v-list-item-avatar class="mr-3 ml-0 mt-0" color="secondary">
            <img
              v-if="notification.actor.profilePicture"
              :src="domainBase + notification.actor.profilePicture"
              :alt="
                notification.actor.name
                  ? notification.actor.name
                  : '@' + notification.actor.username
              "
            />
            <span style="color: white" v-else>{{
              notification.actor.name.trim().length
                ? notification.actor.name.slice(0, 1).toUpperCase() +
                  notification.actor.name
                    .split(" ")[1]
                    .slice(0, 1)
                    .toUpperCase()
                : notification.actor.username.slice(0, 2).toUpperCase()
            }}</span>
          </v-list-item-avatar>
        </v-badge>

        <v-list-item-content>
          <v-list-item-title :title="notification.actor.name">
            <span>
              {{ notification.actor.name }}
            </span>
            <span
              class="username grey--text"
              :title="'@' + notification.actor.username"
            >
              @{{ notification.actor.username }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle :title="notification.verb + ' ' + notification.target">
            {{ notification.verb }}
            <strong class="secondary--text">
              {{ notification.target }}
            </strong>
            <br />
            <span :title="timeSince(notification.created) | capitalize">
              <small>
                {{ timeSince(notification.created) | capitalize }}
              </small>
            </span></v-list-item-subtitle
          >
        </v-list-item-content>
      </v-list-item>
        <v-divider></v-divider>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";
export default {
  name: "Notifications",
  data: () => ({
    notifications: [],
    apiDir: "/robotarium-api/v1.0/notifications-list/",
  }),
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  created() {
    this.retrieveNotifications();
  },
  methods: {
    retrieveNotifications() {
      fetch(this.domainBase + this.apiDir, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.notifications = response;
          this.$emit('unreadNotifications', 0)
        })
        .catch((err) => {
          console.error(err);
        });
    },
    timeSince(dateTime) {
      return moment(dateTime).locale("es").fromNow();
    },
    getIcon(type){
      let icon = ''
      if( type == 'tagged_by_one_user'){
        icon = 'mdi-tag'
      } else if(type == 'reported_by_one_user'){
        icon = 'mdi-alert'
      }
      return icon
    }
  },
  filters: {
    capitalize: function (value) {
      if (!value) return "";
      value = value.toString();
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
  },
};
</script>

<style scoped>
.noti-card {
  position: fixed;
  max-height: 300px;
  height: auto;
  overflow: auto;
  right: 10px;
  top: 62px;
  z-index: 10;
}
.notification:hover{
  background: rgb(209, 209, 209);
  cursor: pointer;
}
.noti-unread{
  background:rgb(209, 209, 209);
}
</style>