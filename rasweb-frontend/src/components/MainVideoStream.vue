<template>
  <div>
    <v-row class="pa-2">
      <v-icon class="live" left>mdi-access-point</v-icon>
      <h3>En vivo</h3>
    </v-row>
    <div class="responsive-content">
      <iframe
        class="skeleton"
        :src="'https://www.youtube.com/embed/' + liveId"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
    <WebSocketLive />
  </div>
</template>
<script>
import { mapState } from "vuex";
import WebSocketLive from "@/components/subcomponents/WebSocketLive.vue";
export default {
  data: () => ({
    liveId: "",
    api_dir: "/coco-api/v1.0/retrieve-liveId/",
  }),
  components:{
    WebSocketLive
  },
  computed: {
    ...mapState(["domain_base", "authentication"]),
  },
  async created() {
    let options = {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Bearer ${this.authentication.accessToken}`,
      },
    };
    let response = await fetch(this.domain_base + this.api_dir, options);
    response = await response.json();
    this.liveId = response.live_id;
  },
};
</script>

<style scoped>
.skeleton {
  background: linear-gradient(90deg, #ededed, #ffffff, #ededed);
  animation-name: load;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
  animation-direction: forwards;
  animation-timing-function: ease;
  background-size: 150% 100%;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
@keyframes load {
  from {
    background-position: 100% 0%;
  }
  to {
    background-position: -100% 0%;
  }
}

.responsive-content {
  position: relative;
  height: 0;
  overflow: hidden;
  padding-bottom: 56.2%;
  margin-bottom: 20px;
}

.live {
  animation-name: live_animation;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
  animation-direction: forwards;
  animation-timing-function: ease;
  color: #BE0707;
}
@keyframes live_animation {
  from {
    color: #BE0707;
  }
  to {
    color: #be070700;
  }
}
</style>