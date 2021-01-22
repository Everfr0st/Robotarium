<template>
  <v-container fluid class="chat-list"  >
    <v-row  justify="end" class="pa-0">   
      <div v-for="(chat,index) in chats" :key="index">
          <ActiveChat :id="`chat_${chat.username}`" :chat="chat" v-on:close="deleteChat" :index="index"/>
      
      </div>
    </v-row>
  </v-container>
</template>
<script>
import { mapState } from "vuex";
import { mapMutations } from "vuex";
import ActiveChat from "@/components/ActiveChat.vue";

export default {

  name: "ActiveChatList",
  components: {
    ActiveChat,
  },
  data: () => ({
    closedChats : []
  }),
  computed: {
  ...mapState(["chats"]), 
  },
  methods:{
    ...mapMutations(["deleteChatfromlist"]),
    deleteChat(chat){
      this.deleteChatfromlist(chat.index);
      let chatCard = document.getElementById('chat_'+chat.username)
      //chatCard.parentNode.removeChild(chatCard);
      this.closedChats.push(chat.username)

    }
  },
  beforeUpdated(){
  }
  
};
</script>
<style  scoped>
.chat-list{
  display: block;
  position: fixed;
  bottom: -15px;
  left: 0px;
  height: auto;
  z-index: 10;
}
@media (min-width: 1264px){
    .chat-list{
    display: block;
    position: fixed;
    bottom: -15px;
    left: 0px;
    width: 90vw;
    height: auto;
  }
}
@media (max-width: 1264px){
    .chat-list{
    display: none;

  }
}

</style>