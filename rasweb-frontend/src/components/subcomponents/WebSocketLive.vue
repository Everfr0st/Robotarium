<template>
  <div style="position: relative;">
    <div class="camera-name">

    <h3 >Cámara {{number == 'one'? '1': '2'}}</h3>
    </div>
    <v-skeleton-loader
      v-if="!isActive && !live.isActive"
      min-height="300"
      type="card"
    ></v-skeleton-loader>
    <img v-if="isActive" :src="'data:image/png;base64,'+img_text" />
  </div>
</template>

<script>
import {mapState, mapMutations} from "vuex";
export default {
    data: () => ({
    liveId: "",
    api_dir: "/robotarium-api/v1.0/retrieve-liveId/",
    img_text: '',
    canvas_obj: '',
    isActive : false,
  }),
  props: ["number"],
  computed:{
      ...mapState(["ws_base", "live"])
  },
  created(){
      
      this.connect();
  },
  mounted(){
    
  },
  methods: {
    ...mapMutations(["updateLiveObj"]),
    connect() { 'ws://127.0.0.1:8000{}/'
      this.websocket = new WebSocket(
        "ws://" + this.ws_base + "/ws/live-main-stream/" + this.number + "/"
      );
      let aux_webSocket = this.websocket;
      this.websocket.onopen = () => {
        console.info("conectado exitosamente!");
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          //console.log(JSON.parse(data))
          const socket_data = JSON.parse(data);
          this.img_text = socket_data.img_data;
          this.isActive = true;
          if (this.number == "one"){
            let liveObj = {
              'time_elapsed': socket_data.time_elapsed,
              'isActive': this.isActive
            }
            this.updateLiveObj(liveObj)
          }

        };
      };
      this.websocket.onclose = () => {
        if (this.number == "one"){
            let liveObj = {
              'time_elapsed': '',
              'isActive': false
            }
            this.updateLiveObj(liveObj)
          }
       
      };
    },
  },
};
</script>

<style scoped>
  img{
    width: 100%;
    height: auto;
  }
.camera-name{
  background: rgba(0,0,0,0.3);
  width: 100%;
  position: absolute;
  top: 0%;
  padding: 5px 15px;
  color: rgba(255,255,255, 0.8)
}
</style>