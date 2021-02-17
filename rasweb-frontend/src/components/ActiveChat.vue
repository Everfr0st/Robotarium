<template>
  <div>
    <v-card
      class="ma-1 chat-card"
      :style="'right: ' + index * position + 'px;'"
      :id="'chat-card-' + chat.username"
      elevation="3"
    >
      <v-card-title
        @click="toggletChat(chat.username, 1)"
        class="white--text chat-header"
      >
        <v-badge bottom overlap dot :color="chat.online ? 'green' : 'grey'">
          <v-avatar size="30" v-if="chat.profilePicture">
            <img :src="chat.profilePicture" :alt="chat.name" />
          </v-avatar>
          <v-avatar color="secondary" size="30" v-else>
            <span v-if="chat.name.trim().length" style="color: white">{{
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
          :title="chat.name.trim().length ? chat.name : '@' + chat.username"
          >{{ chat.name.trim().length ? chat.name : "@" + chat.username }}</span
        >

        <v-spacer></v-spacer>

        <v-btn color="white" icon small>
          <v-icon @click="toggletChat(chat.username, 0)" small
            >mdi-window-minimize</v-icon
          >
        </v-btn>
        <v-btn @click="closeChat()" color="white" icon small>
          <v-icon small>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text class="pa-0 pt-4" style="position: relative">
        <v-container
          style="position: absolute; top: -8px; left: -10%; z-index: 10"
          fluid
          class="ma-0 pa-0"
          v-if="messages.length"
        >
          <div class="chat-date">
            {{ date }}
          </div>
        </v-container>
        <v-container class="chat-messages">
          <span v-if="seen">
            {{ seenMessage }}
          </span>
          <v-card-text class="ma-0 pa-0" v-if="typing">
            <v-row align="center" class="px-4 mt-2 pb-1">
              <v-avatar size="20" v-if="chat.profilePicture">
                <img :src="chat.profilePicture" :alt="chat.name" />
              </v-avatar>
              <v-avatar color="secondary" size="20" v-else>
                <span v-if="chat.name" style="color: white">{{
                  chat.name.split(" ")[0].slice(0, 1)
                }}</span>
                <span v-else style="color: white">{{
                  chat.username.slice(0, 1).toUpperCase()
                }}</span>
              </v-avatar>
              <span class="ml-1">Escribiendo </span>
              <div class="fb-chat">
                <div class="fb-chat--bubbles">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </v-row>
          </v-card-text>
          <v-card
            elevation="0"
            color="white"
            class="mt-1 mb-1 white--text"
            v-for="(message, index) in messages"
            :key="index"
          >
            <v-lazy>
              <v-card-text
                :class="
                  message.sender == selfUser.username
                    ? 'ml-auto outgoing-message'
                    : 'incomming-message'
                "
              >
                <p
                  :title="
                    message.text.length > 50
                      ? message.text.substr(0, 50) + '...'
                      : message.text.substr(0, 50)
                  "
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
                >
                  {{ message.send.split("-")[1] }}
                  <span>
                    <v-icon
                      title="Visto"
                      class="pb-1 ml-1"
                      v-if="message.sender == selfUser.username && message.read"
                      color="white"
                      x-small
                      >mdi-check-all</v-icon
                    >
                    <v-icon
                      title="No leído"
                      class="pb-1"
                      v-if="
                        message.sender == selfUser.username && !message.read
                      "
                      color="white"
                      small
                      >mdi-check</v-icon
                    >
                  </span>
                </small>
              </v-card-text>
            </v-lazy>
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
          class="text-input"
          @keyup.enter="sendMessage()"
          @keyup="typingMessage()"
          @focus="seenText"
          block
          v-model="message"
          label="Envía un mensaje..."
          type="text"
          solo
          autocomplete="off"
        ></v-text-field>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { sendNotificationViaWS } from "../auxfunctions/DomFunctions.js";
import moment from "moment";
var contador = 0;
export default {
  name: "ActiveChat",
  data: () => ({
    websocket: null,
    message: "",
    date_send: "",
    room: null,
    typing: false,
    messages: [],
    position: 255,
    loading: true,
    seen: false,
    seenMessage: "",
    apiDir: "/robotarium-api/v1.0/chat/chat-messages",
  }),
  props: ["chat", "index"],
  computed: {
    ...mapState(["selfUser", "wsBase", "domainBase"]),
    date: function () {
      if (this.messages.length) {
        return moment(this.messages[this.messages.length - 1])
          .locale("es")
          .format("D MMM, YYYY");
      }
    },
    time: function () {
      let date = this.scheduleInfo.date;
      return moment(date + " " + this.scheduleInfo.start_time)
        .locale("es")
        .format("hh:mm a");
    },
  },
  mounted() {
    this.ApiComunication(this.selfUser.username, this.chat.username);
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
          chat_messages.style = `bottom: -295px;
        right: ${this.index * this.position}px`;
        }
      } catch {}
    },
    sendMessage() {
      if (this.message.length) {
        this.websocket.send(
          JSON.stringify({
            type: "chat_message",
            conversation: this.room,
            sender: this.selfUser.username,
            receiver: this.chat.username,
            text: this.message,
            read: false,
          })
        );

        this.message = "";
        let sockedData = {
          type: "new_msg",
          sender: this.selfUser.username,
          receiver: this.chat.username,
        };
        sendNotificationViaWS(sockedData, this.wsBase, this.chat.username);
      }
    },
    typingMessage() {
      let sender = this.selfUser.username;
      if (this.message.length) {
        this.websocket.send(
          JSON.stringify({
            type: "type_message",
            sender: sender,
            receiver: this.chat.username,
            typing: true,
          })
        );
      } else {
        this.websocket.send(
          JSON.stringify({
            type: "type_message",
            sender: sender,
            receiver: this.chat.username,
            typing: false,
          })
        );
      }
    },
    seenText() {
      if (this.chat.username != this.selfUser.username) {
        let sender = this.selfUser.username;
        this.websocket.send(
          JSON.stringify({
            type: "seen_message",
            sender: sender,
            receiver: this.chat.username,
            seen: true,
            room: this.room,
          })
        );
      }
    },
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol + this.wsBase + "/ws/chat/" + this.room + "/"
      );
      this.websocket.onopen = () => {
        /* console.info("conectado exitosamente!", this.room); */
        this.websocket.onmessage = ({ data }) => {
          const socketData = JSON.parse(data);

          if (
            socketData.type === "type_message" &&
            socketData.sender != this.selfUser.username
          ) {
            this.typing = socketData.typing;
          } else if (socketData.type === "chat_message") {
            this.messages.unshift(socketData);
          } else if (socketData.type === "seen_message") {
            if (socketData.receiver == this.selfUser.username) {
              this.checkSeen();
            } else {
              this.$root.$emit("unreadMsgs");
            }
          }
        };
      };
      this.websocket.onclose = () => {
        this.websocket = null;
      };
    },
    closeChat() {
      this.websocket.close();
      this.$emit("close", { username: this.chat.username, index: this.index });
    },
    checkSeen() {
      this.messages.forEach((message) => {
        if (message.sender == this.selfUser.username && message.read == false) {
          message.read = true;
        }
      });
    },
    ApiComunication(sender, receiver) {
      fetch(
        this.domainBase +
          this.apiDir +
          `?sender=${sender}&receiver=${receiver}`,
        {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
        .then((response) => response.json())
        .then((response) => {
          if (response.conversation_created == undefined) {
            this.messages = response;
            this.date_send = response[response.length - 1].send.split("-")[0];
            this.room = response[0].conversation;
          } else if (
            response.error == undefined &&
            response.conversation_created != undefined
          ) {
            this.room = response.conversation;
          } else {
            console.error("Unexpected error have ocurred!!");
          }
          if (this.room != null) {
            this.connect();
          }
          this.loading = false;
          this.message = "";
        });
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
  z-index: 10;
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
  border-radius: 2px;
}
.outgoing-message {
  background: #0a4a73;
  width: auto;
  max-width: 75%;
  float: rigth;
  color: white;
  padding: 5px 5px 5% 5px;
  position: relative;
  border-right: 0px;
  border-radius: 10px 0px 10px 10px;
}

.incomming-message {
  background: #d96334;
  width: auto;
  max-width: 75%;
  padding: 5px 5px 5% 5px;
  position: relative;
  border-left: 0px;
  border-radius: 0px 10px 10px 10px;
}

.text-input {
  border-top: 1px solid rgb(197, 197, 197);
}
.message-time {
  font-size: 6pt;
  color: white;
  position: absolute;
  bottom: -3px;
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

.fb-chat {
  background-color: transparent;
  width: 100px;
  line-height: 60px;
  display: block;
  border-radius: 30%/50%;
  position: absolute;
  left: 80px;
  bottom: -15px;
}
.fb-chat--bubbles {
  text-align: center;
}
.fb-chat--bubbles span {
  display: inline-block;
  background-color: #b6b5ba;
  width: 5px;
  height: 5px;
  border-radius: 100%;
  margin-right: 3px;
  animation: bob 2s infinite;
}
.fb-chat--bubbles span:nth-child(1) {
  animation-delay: -1s;
}
.fb-chat--bubbles span:nth-child(2) {
  animation-delay: -0.85s;
}
.fb-chat--bubbles span:nth-child(3) {
  animation-delay: -0.7s;
  margin-right: 0;
}

@keyframes bob {
  10% {
    transform: translateY(-5px);
    background-color: #9e9da2;
  }
  50% {
    transform: translateY(0);
    background-color: #b6b5ba;
  }
}
</style>