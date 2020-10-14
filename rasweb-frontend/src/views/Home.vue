<template>
  <div>
      <v-container>
        <v-row>
          <ActiveChat/>
        </v-row>
      </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import ActiveChat from "@/components/ActiveChat.vue";
export default {
  name: "Home",
  data: () => ({

    loaded: false,

  }),
  components: {
    ActiveChat,
  },

};
</script>
