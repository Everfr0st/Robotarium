<template>
  <div>
      <h1>Websockets</h1>
    <canvas id="textCanvas"> </canvas>
    <img :src="'data:image/png;base64,'+img_text" />
    <p >{{img_text}}</p>
  </div>
</template>

<script>
import {mapState} from "vuex";
export default {
    data: () => ({
    liveId: "",
    api_dir: "/coco-api/v1.0/retrieve-liveId/",
    img_text: '',
    canvas_obj: '',
  }),
  computed:{
      ...mapState(["ws_base"])
  },
  created(){
      
      this.connect();
  },
  mounted(){
    
  },
  methods: {
    connect() {
      this.websocket = new WebSocket(
        "ws://" + this.ws_base + "/ws/live/main-stream"
      );
      console.log("ws://" + this.ws_base + "/ws/live/main-stream")
      let aux_webSocket = this.websocket;
      this.websocket.onopen = () => {
        console.info("conectado exitosamente!");
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          //console.log(JSON.parse(data))
          const socket_data = JSON.parse(data);
          this.img_text = socket_data.img_data;

          console.log(socket_data.img_data)
        };
      };
      this.websocket.onclose = () => {
       
      };
    },
  },
};
</script>

<style scoped>
    p{
           word-break: break-all;
    white-space: normal;
    }
</style>