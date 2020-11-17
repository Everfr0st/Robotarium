<template>
  <div class="ma-2">
    <v-row>
      <v-icon class="live" left>mdi-access-point</v-icon>
      <h3>En vivo</h3>
    </v-row>
    <v-row class="live-container">
      <v-col class="ma-0 pa-0">
        <WebSocketLive number="one" />
      </v-col>
      <v-col class="ma-0 pa-0">
        <WebSocketLive number="two" />
      </v-col>
      <div class="live-bar" v-if="live.isActive">
        <v-row>
          <p>
            <v-icon class="ml-3 mb-1 live" color="primary" small
              >mdi-checkbox-blank-circle</v-icon
            >
            En vivo

            <span class="live-time-elapsed">
              {{ live.time_elapsed }}
            </span>
          </p>
        </v-row>
      </div>
    </v-row>
  </div>
</template>
<script>
import { mapState } from "vuex";
import WebSocketLive from "@/components/subcomponents/WebSocketLive.vue";
export default {
  data: () => ({
    liveId: "",
    api_dir: "/robotarium-api/v1.0/retrieve-liveId/",
  }),
  components: {
    WebSocketLive,
  },
  computed: {
    ...mapState(["domain_base", "authentication", "live"]),
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
.live-container {
  position: relative;
  border-radius: 5px;
}
.live-bar {
  position: absolute;
  bottom: 6px;
  padding: 3px 15px;
  background: rgba(0, 0, 0, 0.3);
  height: 30px;
  width: 100%;
  -webkit-user-select: none;
    -moz-user-select: none;
    -khtml-user-select: none;
    -ms-user-select:none;
}
p {
  font-size: 12pt;
  color: white;
}
.live-time-elapsed {
  font-size: 10pt;
  margin-left: 5px;
}
</style>