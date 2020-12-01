<template>
  <div v-if="liveObj.started" style="position: relative">
    <div class="camera-name">
      <h3 v-if="number.trim().length">Cámara {{ number == "one" ? "1" : "2" }}</h3>
      <h3 v-else>{{ robotarium }}</h3>
    </div>

    <img :src="'data:image/png;base64,' + img_text" />
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  data: () => ({
    liveId: "",
    api_dir: "/ws/live-main-stream/",
    img_text: "",
    liveObj: '',
  }),
  props: ["number",],
  computed: {
    ...mapState(["wsBase", "live", "robotarium", "domainBase"]),
  },
  created() {
    this.connect();
  },
  mounted() {},
  destroyed() {
    this.websocket.close();
  },
  methods: {
    ...mapMutations(["updateLiveObj"]),
    connect() {
      let dir = this.number.trim().length
        ? this.wsBase + this.api_dir + this.number
        : this.wsBase + this.api_dir + this.robotarium.robot;
        console.log(dir)
      this.websocket = new WebSocket("ws://" + dir + "/"); //Manage secure websocket
      this.websocket.onopen = () => {
        console.info("conectado exitosamente!");
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          //console.log(JSON.parse(data))
          const socket_data = JSON.parse(data);
          this.img_text = socket_data.img_data;
          if (this.number == "one") {
            let liveObj = {
              time_elapsed: socket_data.time_elapsed,
              started: socket_data.started,
              finished: socket_data.finished,
            };

            this.updateLiveObj(liveObj);
          }
        };
      };
      this.websocket.onclose = () => {
        if (this.number == "one") {
          let liveObj = {
            started: false,
            time_elapsed: "",
          };
          this.updateLiveObj(liveObj);
        }
      };
    },
  },
};
</script>

<style scoped>
img {
  width: 100%;
  height: auto;
}
.camera-name {
  background: rgba(0, 0, 0, 0.3);
  width: 100%;
  position: absolute;
  top: 0%;
  padding: 5px 15px;
  color: rgba(255, 255, 255, 0.8);
}
</style>