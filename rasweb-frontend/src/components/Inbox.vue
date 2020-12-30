<template>
  <v-card id="inbox" elevation="5" class="inbox px-0" width="350" max-width="350">
    <v-card-title class="pa-0 ml-3 mt-3"> Mensajes </v-card-title>
    <v-card-subtitle class="mt-2" v-if="!inbox.length">Aún no tienes mensajes 😵</v-card-subtitle>
    <v-card-text class="px-0 pt-0 mx-0 pb-0" v-for="(conversation, index) in inbox"
        :key="index">
        <ChatElement v-on:unreadMessages="updateCountUnreadMessages" :index="index" :dialog="conversation" />
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import ChatElement from "../components/ChatElement.vue"
export default {
  name: "Inbox",
  components:{
    ChatElement,
  },
  data: () => ({
    inbox: [],
    apiDir: "/robotarium-api/v1.0/inbox/",
    unreadMessages: 0,
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
    updateCountUnreadMessages(unreadMessages){
      this.unreadMessages += unreadMessages;
      this.$emit('unreadMessages', this.unreadMessages)
      this.unreadMessages = 0;
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