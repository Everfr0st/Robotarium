<template>
  <div>
    {{ topicName }}
    <v-select
      @change="subscribe2Topic"
      label="Topic"
      return-object
      item-text="name"
      placeholder=""
      item-value="name"
      v-model="topicName"
      :items="items"
    >
    </v-select>
    <v-btn color="error" @click="unSubscribe">Parar</v-btn>
    <p v-if="connected" class="success--text">Conectado a {{ wsAddress }}</p>
    <p v-else class="error--text">Desconectado</p>
  </div>
</template>

<script>
// 0.26 y 1.82
import ROSLIB from "roslib";
var radius = 50;
export default {
  name: "Joistick",
  data: () => ({
    img: "",
    topicName: "",
    items: [
      {
        name: "/camera/rgb/image_raw",
        messageType: "sensor_msgs/Image",
      },
      {
        name: "/camera/rgb/image_raw/compressed",
        messageType: "sensor_msgs/CompressedImage",
      },
      {
        name: "/camera/rgb/image_raw/compressedDepth",
        messageType: "sensor_msgs/CompressedImage",
      },
      {
        name: "/camera/rgb/image_raw/theora",
        messageType: "theora_image_transport/Packet",
      },
    ],
    ros: null,
    topic: "",
    message: "",
    wsAddress: "ws://0.0.0.0:9090",
    listener: null,
    connected: false,
  }),
  mounted() {
    this.connect();
  },
  computed: {},
  methods: {
    connect() {
      this.ros = new ROSLIB.Ros({
        url: this.wsAddress,
      });

      this.ros.on("connection", () => {
        console.log("connected to websocket server rosbridge");
        this.connected = true;
      });
      this.ros.on("error", (error) => {
        console.error(error);
      });
      this.ros.on("close", () => {
        console.log("connection closed");
      });
    },
    subscribe2Topic() {
      this.setTopic();
      this.listenData();
    },
    setTopic() {
      this.topic = new ROSLIB.Topic({
        ros: this.ros,
        name: this.topicName.name,
        messageType: this.topicName.messageType,
      });
    },

    listenData() {
      this.topic.subscribe((data) => {
          this.$emit("robotView", data.data);
      });
    },
    unSubscribe() {
      this.topic.unsubscribe();
    },
  },
};
</script>

<style scoped>
#zone_joystick {
  max-width: 300px;
}
</style>