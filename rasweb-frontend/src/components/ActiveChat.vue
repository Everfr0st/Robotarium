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
          :title="chat.name ? chat.name : '@' + chat.username"
          >{{ chat.name ? chat.name : "@" + chat.username }}</span
        >

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
      <v-card-text class="pa-0 pt-4" style="position: relative">
        <v-container
          style="position: absolute; top: -8px; left: -10%; z-index: 1000"
          fluid
          class="ma-0 pa-0"
          v-for="(message, index) in messages"
          :key="index"
        >
          <div v-if="index === 0" class="chat-date">
            {{ message.send.split("-")[0] }}
          </div>
          <div v-else class="chat-date">
            {{
              message.send.split("-")[0] ==
              messages[index - 1].send.split("-")[0]
                ? ""
                : message.send.split("-")[0]
            }}
          </div>
        </v-container>
        <v-container class="chat-messages">
          <v-card-text class="ma-0 pa-0" v-if="typing">
            <v-row class="ml-0">
              <v-avatar size="20" v-if="chat.profile_picture">
                <img :src="chat.profile_picture" :alt="chat.name" />
              </v-avatar>
              <v-avatar color="secondary" size="20" v-else>
                <span v-if="chat.name" style="color: white">{{
                  chat.name.split(" ")[0].slice(0, 1)
                }}</span>
                <span v-else style="color: white">{{
                  chat.username.slice(0, 1).toUpperCase()
                }}</span>
              </v-avatar>
              <span class="ml-1">Escribiendo...</span>
            </v-row>
          </v-card-text>

          <v-card
            elevation="0"
            color="white"
            class="mt-1 mb-1 white--text"
            v-for="(message, index) in messages"
            :key="index"
          >
            <v-card-text
              :class="
                message.sender == self_user
                  ? 'ml-auto outgoing-message'
                  : 'incomming-message'
              "
            >
              <p
                :title="message.text"
                style="margin: 0px; padding: 0px"
                class="white--text"
              >
                {{ message.text }}
              </p>
              <small
                :title="
                  message.send.split('-')[0] +
                  'a las' +
                  message.send.split('-')[1]
                "
                class="message-time"
                >{{ message.send.split("-")[1] }}</small
              >
            </v-card-text>
          </v-card>
          <v-btn
          v-if="loading"
            text
            class="ma-2"
            :loading="loading"
            :disabled="loading"
            color="secondary"
          >
          </v-btn>
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
    message: "",
    typing: false,
    loading: true,
    messages: [],
    position: 255,
  }),
  props: ["chat", "index"],
  computed: {
    ...mapState(["chats", "self_user"]),
  },

  async created() {
    const api_dir = `/coco-api/v1.0/chat/chat-messages?sender=${this.self_user}&receiver=${this.chat.username}`;
    let response = await fetch(web_domain + api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
    });
    response = await response.json();
    this.messages = response;
    this.loading = false;
},
  beforeDestroy() {
    this.messages = [];
  },
  methods: {
    ...mapMutations(["deleteChatfromlist"]),
    toggletChat(username, action) {
      let chat_messages = document.getElementById("chat-card-" + username);

      try {
        let get_chat_position = chat_messages.getBoundingClientRect();
        if (
          action &&
          event.srcElement.className !==
            "v-icon notranslate v-icon--link mdi mdi-window-minimize theme--light"
        ) {
          chat_messages.style = `bottom: 10px;
        right: ${this.index * this.position}px`;
        } else {
          chat_messages.style = `bottom: -285px;
        right: ${this.index * this.position}px`;
        }
      } catch {}
    },
  },
};
</script>
<style  scoped>
.chat-card {
  width: 250px;
  height: 345px;
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
  display: flex;
  flex-direction: column-reverse;
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
.outgoing-message {
  background: #0a4a73;
  width: auto;
  max-width: 60%;
  float: rigth;
  color: white;
  padding: 5px 5px 18px 5px;
  position: relative;
}
.outgoing-message::after {
  content: "";
  width: 0;
  height: 0;
  border-right: 5px solid #0a4a73;
  border-top: 5px solid transparent;
  border-left: 5px solid transparent;
  border-bottom: 5px soli#0A4A73;
  transform: rotate(180deg);
  position: absolute;
  top: 0px;
  right: -7px;
}
.incomming-message {
  background: #be0707;
  width: auto;
  max-width: 60%;
  padding: 5px 5px 18px 5px;
  position: relative;
}
.incomming-message::after {
  content: "";
  width: 0;
  height: 0;
  border-right: 5px solid #be0707;
  border-top: 5px solid transparent;
  border-left: 5px solid transparent;
  border-bottom: 5px solid#BE0707;
  transform: rotate(-90deg);
  position: absolute;
  top: 0px;
  left: -4px;
}
.message-time {
  font-size: 7pt;
  color: white;
  position: absolute;
  bottom: 0px;
  right: 3px;
}
.chat-date {
  font-size: 10pt;

  color: white;
  max-width: 100px;
  width: auto;
  background: rgba(0, 0, 0, 0.7);
  text-align: center;
  border-radius: 5px;
  margin: 10px 0px 10px 40%;
}
</style>