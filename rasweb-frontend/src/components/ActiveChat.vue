<template>
  <div>
    <v-card
      class="ma-1 chat-card"
      :style="'right: ' + index * position + 'px;'"
      :id="'chat-card-' + chat.username"
    >
      <v-card-title
        @click="toggletChat(chat.username, 1)"
        class="white--text chat-header"
      >
        <v-badge bottom overlap dot :color="chat.color">
          <v-avatar size="30" v-if="chat.profile_picture">
            <img :src="chat.profile_picture" :alt="chat.name" />
          </v-avatar>
          <v-avatar color="secondary" size="30" v-else>
            <span v-if="chat.name" style="color: white">{{
              chat.name.split(" ")[0].slice(0, 1)
            }}</span>
            <span v-else style="color: white">{{
              chat.username.slice(0, 1).toUpperCase()
            }}</span>
          </v-avatar>
        </v-badge>

        <span
          class="ml-3 d-inline-block text-truncate"
          style="font-size: 11pt; max-width: 130px"
          :title="chat.name?chat.name:'@'+chat.username"
          >{{ chat.name?chat.name: '@'+chat.username }}</span>
     
        <v-spacer></v-spacer>

        <v-btn color="white" icon small>
          <v-icon @click="toggletChat(chat.username, 0)" small
            >mdi-window-minimize</v-icon
          >
        </v-btn>
        <v-btn @click="deleteChatfromlist(chat)" color="white" icon small>
          <v-icon small>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pa-0">
        <v-container class="chat-messages">
          {{ messages }}
        </v-container>
      </v-card-text>
      <v-card-actions class="ma-0 pa-0">
        <v-text-field
          block
          v-model="message"
          label="Envía un mensaje..."
          type="text"
          solo
        ></v-text-field>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { mapMutations } from "vuex";
const web_domain = "http://127.0.0.1:8000";
export default {
  name: "ActiveChat",
  data: () => ({
    message: '',
    messages: [],
    position: 255,
    
  }),
  props: ["chat", "index"],
  computed: {
    ...mapState(["chats","self_user"]),
  },
  async created(){
    const api_dir = `/coco-api/v1.0/chat/chat-messages?sender=${this.self_user}&receiver=${this.chat.username}`;
    let response = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    response = await response.json();
    this.messages = response
    console.log(response)
  },
  methods: {
    ...mapMutations(["deleteChatfromlist"]),
    toggletChat(username, action) {
      let chat_messages = document.getElementById("chat-card-" + username);
      let get_chat_position = chat_messages.getBoundingClientRect();
      console.log(event.srcElement);
      if (
        action &&
        event.srcElement.className !== "v-icon notranslate v-icon--link mdi mdi-window-minimize theme--light") {
        chat_messages.style =  `bottom: 10px;
        right: ${this.index * this.position}px`;
      } else {
        chat_messages.style = `bottom: -285px;
        right: ${this.index * this.position}px`;
      }
    },
  },
};
</script>
<style  scoped>
.chat-card {
  width: 250px;
  height: 335px;
  overflow: hidden;
  position: absolute;
  bottom: 10px;
}
.chat-header {
  background-color: #be0707;
  color: white;
  height: 40px;
  margin: 0px;
  padding: 0px 10px;
}
.chat-header:hover {
  cursor: pointer;
}
.chat-messages {
  height: 250px;
  overflow: auto;
}
.chat-messages::-webkit-scrollbar {
  width: 3px; /* Tamaño del scroll en vertical */
  height: 3px; /* Tamaño del scroll en horizontal */
  /* display: none; Ocultar scroll */
}
/* Ponemos un color de fondo y redondeamos las esquinas del thumb */
.chat-messages::-webkit-scrollbar-thumb {
  background: #be0707;
  border-radius: 4px;
}
</style>