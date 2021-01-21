<template>
  <div id="zone_joystick">
    <v-container>
      <small>Joistick</small>
      <p class="pt-0">Velocidad ({{ speed }}%)</p>
      <v-slider
        v-model="speed"
        :color="color"
        thumb-label
        track-color="grey"
        always-dirty
        min="0"
        max="100"
        @change="go2Dir"
        :disabled="!connected"
      >
      </v-slider>
      <v-row justify="center">
        <v-btn :disabled="!connected" color="info" @mousedown="forward" fab>
          <v-icon>mdi-arrow-up</v-icon>
        </v-btn>
      </v-row>
      <v-row class="mt-4" justify="space-around">
        <v-btn :disabled="!connected" color="info" @mousedown="left" fab>
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-btn :disabled="!connected" color="error" @mousedown="stop" fab>
          <v-icon>mdi-stop</v-icon>
        </v-btn>
        <v-btn :disabled="!connected" color="info" @mousedown="right" fab>
          <v-icon>mdi-arrow-right</v-icon>
        </v-btn>
      </v-row>
      <v-row class="mt-4" justify="center">
        <v-btn :disabled="!connected" color="info" @mousedown="backward" fab>
          <v-icon>mdi-arrow-down</v-icon>
        </v-btn>
      </v-row>
    </v-container>
    
  </div>
</template>

<script>
// 0.26 y 1.82
import ROSLIB from "roslib";
var radius = 50;
export default {
  name: "Joistick",
  props: ['wsAddress'],
  data: () => ({
    speed: 50,
    dir: 0,
    interval: null,
    isPlaying: false,
    connected: false,
    ros: null,
    topic: "",
    message: "",
    
  }),
  mounted() {
    //this.joistickFunction();
    this.connect();
    //joistick_div.style = "position: relative;"
  },
  computed: {
    color() {
      if (this.speed < 25) return "red";
      if (this.speed < 50) return "orange";
      if (this.speed <= 75) return "blue";
      if (this.speed > 75) return "green";
      return "red";
    },
  },
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
    setTopic() {
      this.topic = new ROSLIB.Topic({
        ros: this.ros,
        name: "/cmd_vel",
        messageType: "geometry_msgs/Twist",
      });
    },

    forward() {
      this.dir = 1;
      this.message = new ROSLIB.Message({
        linear: { x: (this.speed / 100) * 0.26, y: 0, z: 0 },
        angular: { x: 0, y: 0, z: 0 },
      });
      this.publishData();
    },
    backward() {
      this.dir = 3;
      this.message = new ROSLIB.Message({
        linear: { x: (-this.speed / 100) * 0.26, y: 0, z: 0 },
        angular: { x: 0, y: 0, z: 0 },
      });
      this.publishData();
    },
    left() {
      this.dir = 4;
      this.message = new ROSLIB.Message({
        linear: { x: 0.0, y: 0, z: 0 },
        angular: { x: 0.0, y: 0, z: (this.speed / 100) * 1.86 },
      });
      this.publishData();
    },
    right() {
      this.dir = 2;
      this.message = new ROSLIB.Message({
        linear: { x: 0.0, y: 0, z: 0 },
        angular: { x: 0.0, y: 0, z: (-this.speed / 100) * 1.86 },
      });
      this.publishData();
    },
    stop() {
      this.dir = 0;
      this.message = new ROSLIB.Message({
        linear: { x: 0.0, y: 0, z: 0 },
        angular: { x: 0.0, y: 0, z: 0 },
      });
      this.publishData();
    },
    publishData() {
      setInterval(() => {
        this.setTopic();
        this.topic.publish(this.message);
      }, 30);
    },
    decrement() {
      this.speed--;
    },
    increment() {
      this.speed++;
    },
    go2Dir() {
      switch (this.dir) {
        case 1:
          this.forward();
          break;
        case 2:
          this.right();
          break;
        case 1:
          this.backward();
          break;
        case 1:
          this.left();
          break;

        default:
          this.stop();
          break;
      }
    },
  },
};
</script>

<style scoped>
#zone_joystick {
}
</style>