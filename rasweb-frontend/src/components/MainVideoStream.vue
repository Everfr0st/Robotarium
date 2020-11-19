<template>
  <div class="ma-2 pr-5">
    <v-row>
      <v-icon :class="live.started && !live.finished ? 'live' : ''" left
        >{{live.started && !live.finished ? 'mdi-access-point' : 'mdi-access-point-off'}}</v-icon
      >
      <h3>{{ live.started && !live.finished ? "En vivo" : "Robotarium" }}</h3>
    </v-row>
    <v-row v-if="live.finished">
      <v-card class="body">
        <div class="static">
          <div>
            
            <h2 class="ml-2 ">Transmisión finalizada</h2>
          </div>
        </div>
        <div class="scan"></div>
      </v-card>
      
    </v-row>
    <v-row v-else-if="!live.started">
      <v-skeleton-loader width="100%" min-heigth="350" type="card"></v-skeleton-loader>
    </v-row>

    <v-row class="live-container">
      <v-col class="ma-0 pa-0">
        <WebSocketLive number="one" />
      </v-col>
      <v-col class="ma-0 pa-0">
        <WebSocketLive number="two" />
      </v-col>
      <div class="live-bar" v-if="live.started">
        <v-row>
          <p>
            <v-icon class="live ml-3 mb-1" color="primary" small
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
  color: #be0707;
}
@keyframes live_animation {
  from {
    color: #be0707;
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
  -ms-user-select: none;
}
p {
  font-size: 12pt;
  color: white;
}
.live-time-elapsed {
  font-size: 10pt;
  margin-left: 5px;
}

.body {
  height: 55vh;
  width: 100%;
}
.body {
  background-image: radial-gradient(transparent, hsla(0, 0%, 0%, 0.85)),
    linear-gradient(transparent 75%, hsl(0, 0%, 0%) 75%),
    linear-gradient(
      left,
      hsl(0, 0%, 82%) 14.29%,
      hsl(54, 100%, 50%) 14.29%,
      hsl(54, 100%, 50%) 28.57%,
      hsl(184, 100%, 50%) 28.57%,
      hsl(184, 100%, 50%) 42.86%,
      hsl(121, 98%, 42%) 42.86%,
      hsl(121, 98%, 42%) 57.14%,
      hsl(320, 93%, 37%) 57.14%,
      hsl(320, 93%, 37%) 71.43%,
      hsl(349, 100%, 50%) 71.43%,
      hsl(349, 100%, 50%) 85.71%,
      hsl(240, 100%, 38%) 85.71%
    );
  background-image: radial-gradient(transparent, hsla(0, 0%, 0%, 0.85)),
    linear-gradient(transparent 75%, hsl(0, 0%, 0%) 75%),
    linear-gradient(
      to left,
      hsl(0, 0%, 82%) 14.29%,
      hsl(54, 100%, 50%) 14.29%,
      hsl(54, 100%, 50%) 28.57%,
      hsl(184, 100%, 50%) 28.57%,
      hsl(184, 100%, 50%) 42.86%,
      hsl(121, 98%, 42%) 42.86%,
      hsl(121, 98%, 42%) 57.14%,
      hsl(320, 93%, 37%) 57.14%,
      hsl(320, 93%, 37%) 71.43%,
      hsl(349, 100%, 50%) 71.43%,
      hsl(349, 100%, 50%) 85.71%,
      hsl(240, 100%, 38%) 85.71%
    );
  position: relative;
  overflow: hidden;
}
.body:before {
  content: "";
  position: absolute;
  display: block;
  background-image: linear-gradient(
    left,
    hsl(240, 100%, 38%) 14.29%,
    hsl(0, 0%, 0%) 14.29%,
    hsl(0, 0%, 0%) 28.57%,
    hsl(320, 93%, 27%) 28.57%,
    hsl(320, 93%, 27%) 42.86%,
    hsl(0, 0%, 0%) 42.86%,
    hsl(0, 0%, 0%) 57.14%,
    hsl(184, 100%, 50%) 57.14%,
    hsl(184, 100%, 50%) 71.43%,
    hsl(0, 0%, 0%) 71.43%,
    hsl(0, 0%, 0%) 85.71%,
    hsl(0, 0%, 82%) 85.71%
  );
  background-image: linear-gradient(
    to left,
    hsl(240, 100%, 38%) 14.29%,
    hsl(0, 0%, 0%) 14.29%,
    hsl(0, 0%, 0%) 28.57%,
    hsl(320, 93%, 27%) 28.57%,
    hsl(320, 93%, 27%) 42.86%,
    hsl(0, 0%, 0%) 42.86%,
    hsl(0, 0%, 0%) 57.14%,
    hsl(184, 100%, 50%) 57.14%,
    hsl(184, 100%, 50%) 71.43%,
    hsl(0, 0%, 0%) 71.43%,
    hsl(0, 0%, 0%) 85.71%,
    hsl(0, 0%, 82%) 85.71%
  );
  height: 5%;
  width: 100%;
  bottom: 25%;
}

/*********************
  STATIC 
*********************/

.static,
.static div {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  color: rgb(219, 219, 219);
  background-color: rgba(0, 0, 0, 0.2);
}

/*********************
  SCAN LINES
*********************/

.scan,
.scan:before,
.scan:after {
  position: absolute;
  left: 0;
  width: 100%;
  height: 10%;
  background-color: hsla(0, 0%, 0%, 0.13);
  box-shadow: 0 0 10px hsla(0, 0%, 0%, 0.25);
  animation: scan 6s linear infinite;
}
.scan:before,
.scan:after {
  content: "";
  display: block;
  height: 60%;
}
.scan:before {
  top: -350%;
}
.scan:after {
  top: -1100%;
}
@keyframes scan {
  0% {
    top: -20%;
  }
  100% {
    top: 250%;
  }
}
</style>