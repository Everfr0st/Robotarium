<template>
  <v-container>
    <v-row justify="space-around" class="pa-0">
      <v-card width="250" height="335" style="overflow: hidden;">
        <v-card-title class="white--text chat-header">
          <v-badge bottom overlap dot :color="chat.online">
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
            :title="chat.name"
            >{{ chat.name }}</span
          >
          <v-spacer></v-spacer>

          <v-btn color="white" icon small>
            <v-icon small>mdi-window-minimize</v-icon>
          </v-btn>
          <v-btn color="white" icon small>
            <v-icon small>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="pa-0"> 
            <v-container class="chat-messages"> 
                {{chat}}
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
    </v-row>
    <pre>
        {{chat}}
    </pre>
    <pre>
        {{chats}}
    </pre>

  </v-container>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ActiveChat",
  data: () => ({
      message : '',
  }),
  computed: {
    ...mapState(["chat", "chats"]),
    
  },
};
</script>
<style  scoped>
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
.chat-messages{
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