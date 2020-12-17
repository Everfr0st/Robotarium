<template>
  <v-container class="chat-list"  >
    <v-row   justify="end" class="pa-0">   
      <div v-for="(chat,index) in chats" :key="index">
          <ActiveChat v-if="chats.length<=3" :chat="chat" :index="index"/>
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
  data: () => ({}),
  computed: {
  ...mapState(["chats"]), 
  },
  methods:{
    ...mapMutations(["deleteChatfromlist"]),
  }
};
</script>
<style  scoped>
.chat-list{
  position: fixed;
  bottom: -15px;
  left: 0px;
  width: 85%;
  height: auto;
  display: inline-block; 
  z-index: 2;
}
</style>