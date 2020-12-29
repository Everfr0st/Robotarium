<template>
  <v-card elevation="5" class="inbox px-0" width="350" max-width="350">
    <v-card-title class="pa-0 ml-3 mt-3"> Mensajes </v-card-title>
    <v-card-text class="px-0 mx-0 pb-0">
      <v-list-item
        two-line
        v-for="(conversation, index) in inbox"
        :key="index"
        class="notification pl-0"
        @click="addChat2List(conversation.opponent)"
      >
        <v-badge
          bordered
          bottom
          :color="conversation.opponent.online?'green':'grey'"
          offset-x="25px"
          offset-y="25px"
          dot
        >
          <v-list-item-avatar color="secondary">
            <img
              v-if="conversation.opponent.profile_picture"
              :src="domainBase + conversation.opponent.profile_picture"
              :alt="
                conversation.opponent.name
                  ? conversation.opponent.name
                  : '@' + conversation.opponent.username
              "
            />
            <span style="color: white" v-else>{{
              conversation.opponent.name.trim().length
                ? conversation.opponent.name.slice(0, 1).toUpperCase() +
                  conversation.opponent.name
                    .split(" ")[1]
                    .slice(0, 1)
                    .toUpperCase()
                : conversation.opponent.username.slice(0, 2).toUpperCase()
            }}</span>
          </v-list-item-avatar>
        </v-badge>

        <v-list-item-content>
          <v-list-item-title :title="conversation.opponent.name">
            <span>
              {{ conversation.opponent.name }}
            </span>
            <span
              class="username grey--text"
              :title="'@' + conversation.opponent.username"
            >
              @{{ conversation.opponent.username }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle :title="conversation.text">
            {{ conversation.text }}
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <small>
            {{ conversation.send.split("-")[1] }}
          </small>
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "Inbox",
  data: () => ({
    inbox: [],
    apiDir: "/robotarium-api/v1.0/inbox/",
  }),
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  created() {
    this.retrieveMessages();
  },
  methods: {
    ...mapMutations(["addChat2List"]),
    retrieveMessages() {
      fetch(this.domainBase + this.apiDir, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.inbox = response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
.inbox {
  position: fixed;
  max-height: 300px;
  height: auto;
  overflow: auto;
  right: 30px;
  top: 62px;
  z-index: 10;
}
.notification:hover {
  background: rgb(209, 209, 209);
  cursor: pointer;
}
</style>