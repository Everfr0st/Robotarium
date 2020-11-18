<template>
  <div v-if="live.started"  style="position: relative;">
    <div class="camera-name">

    <h3 >Cámara {{number == 'one'? '1': '2'}}</h3>
    </div>
    
    <img :src="'data:image/png;base64,'+img_text" />
  </div>
</template>

<script>
import {mapState, mapMutations} from "vuex";
export default {
    data: () => ({
    liveId: "",
    api_dir: "/ws/live-main-stream/",
    img_text: '',
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
  destroyed(){
    this.websocket.close();
  },
  methods: {
    ...mapMutations(["updateLiveObj"]),
    connect() { 'ws://127.0.0.1:8000{}/'
      this.websocket = new WebSocket(
        "ws://" + this.ws_base + this.api_dir + this.number + "/"
      );
      let aux_webSocket = this.websocket;
      this.websocket.onopen = () => {
        console.info("conectado exitosamente!");
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          //console.log(JSON.parse(data))
          const socket_data = JSON.parse(data);
          this.img_text = socket_data.img_data;
          if (this.number == "one"){
            let liveObj = {
              'time_elapsed': socket_data.time_elapsed,
              'started': socket_data.started,
              'finished': socket_data.finished
            }
            
            this.updateLiveObj(liveObj);
          }

        };
      };
      this.websocket.onclose = () => {
        if (this.number == "one"){
            let liveObj = {
              'started': false,
              'time_elapsed': '',
            }
            this.updateLiveObj(liveObj)
            
          }
          console.log("cerrando websocket.")
       
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