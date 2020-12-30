<template>
  <div :id="`chat_${conversation.opponent}`">
    <v-list-item
      two-line
      :class="conversation.unread_messages? 'chat mt-0 pl-0':'chat mt-0 pl-0'"
      
      @click="addChat2List(conversation.opponent)"
    >
      <v-badge
        bordered
        bottom
        :color="conversation.opponent.online ? 'green' : 'grey'"
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
        <v-list-item-subtitle v-if="!typing" :title="conversation.text">
          <span>
            {{
              conversation.text.length > 25
                ? conversation.text.slice(0, 20) + "..."
                : conversation.text
            }}
          </span>
          <span>
            <v-icon
              small
              :color="
                conversation.sender == selfUser.username ? 'info' : 'success'
              "
            >
              {{
                conversation.sender == selfUser.username
                  ? "mdi-arrow-top-right"
                  : "mdi-arrow-bottom-left"
              }}
            </v-icon>
          </span>
          <v-chip
            x-small
            rigth
            color="info darken-2"
            v-if="conversation.unread_messages"
          >
            <small :title="conversation.unread_messages">
              {{ conversation.unread_messages }}
            </small>
          </v-chip>
        </v-list-item-subtitle>
        <v-list-item-subtitle
          title="Escribiendo..."
          class="primary--text"
          v-else
          >Escribiendo...</v-list-item-subtitle
        >
      </v-list-item-content>
      <v-list-item-action>
        <small :title="dateSend">
          {{ dateSend }}
        </small>
      </v-list-item-action>
    </v-list-item>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "ChatElement",
  props: ["dialog", "index"],
  data: () => ({
    websocket: null,
    typing: false,
    message: "",
    conversation: "",
  }),
  computed: {
    ...mapState(["selfUser", "wsBase"]),
    dateSend: {
      get: function () {
        return this.conversation.send.split("-")[1];
      },
      set: function (val) {},
    },
  },
  created() {
    this.conversation = this.dialog;
    this.connect();
  },
  methods: {
    ...mapMutations(["addChat2List"]),
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol +
          this.wsBase +
          "/ws/chat/" +
          this.conversation.conversation +
          "/"
      );
      this.websocket.onopen = () => {
        console.info(
          "conectado exitosamente inbox!",
          this.conversation.conversation
        );
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));

          const socketData = JSON.parse(data);
          if (
            socketData.type === "type_message" &&
            socketData.sender != this.selfUser.username
          ) {
            this.typing = socketData.typing;
          } else if (socketData.type === "chat_message") {
            this.conversation.text = socketData.text;
            this.conversation.send = socketData.send;
            this.conversation.sender = socketData.sender;
            if(socketData.sender != this.selfUser.username) {
                this.conversation.unread_messages = socketData.unread_messages;
                this.$emit("unreadMessages", this.conversation.unread_messages);
               // this.$emit('moveChat', this.index)
            } 
          } else if (socketData.type == "seen_message" && socketData.receiver == this.selfUser.username) {
            this.conversation.unread_messages = socketData.unread_messages;
            this.$emit("unreadMessages", this.conversation.unread_messages);
          }
        };
      };
      this.websocket.onclose = () => {
      };
      
    },
    firstPlate(){
          var parent = document.getElementById("inbox");
          var currentNode = document.getElementById(`chat_${this.conversation.opponent}`)
          parent.insertBefore(currentNode,parent.children[1])
      }
  },
};
</script>

<style>
.chat:hover {
  background: rgb(209, 209, 209);
}.unread{
    background: rgb(209, 209, 209);;
}
</style>