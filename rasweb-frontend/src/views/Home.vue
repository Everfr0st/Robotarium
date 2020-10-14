<template>
  <div>
      <v-container>
        <v-row>
          <ActiveChatList/>
        </v-row>
      </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import ActiveChatList from "@/components/ActiveChatList.vue";
export default {
  name: "Home",
  data: () => ({

    loaded: false,

  }),
  components: {
    ActiveChatList,
  },

};
</script>
