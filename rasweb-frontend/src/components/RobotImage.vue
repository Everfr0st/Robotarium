<template>
  <div>
    <small>Cámara</small>
    <v-select
      @change="subscribe2Topic"
      label="Topic"
      return-object
      item-text="name"
      placeholder=""
      item-value="name"
      v-model="topicName"
      :items="items"
      :disabled="!connected"
    >
    </v-select>
    <small
      >* Topic recomendado:
      <strong>/{{robot.name}}/camera_node/image/compressed</strong></small
    >
    <v-btn
      :disabled="!connected"
      color="info"
      v-if="!addCustomTopic"
      @click="addCustomTopic = true"
      class="mt-2"
      ><span class="capitalize">Añadir topic personalizado</span></v-btn
    >
    <v-row class="pt-0" v-else>
      <v-col sm="6">
        <v-text-field v-model="customTopic" label="Topic"> </v-text-field>
      </v-col>
      <v-col sm="6">
        <v-text-field v-model="customMsgType" label="Msg Type"> </v-text-field>
      </v-col>

      <v-col sm="12">
        <v-btn @click="addTopic" color="accent darken-2" block> Añadir </v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar">
      {{ snackMsg }}

      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
// 0.26 y 1.82
import ROSLIB from "roslib";
var radius = 50;
export default {
  name: "Joistick",
  props: ["wsAddress", "robot"],
  data: () => ({
    img: "",
    topicName: "",
    customTopic: "",
    customMsgType: "",
    addCustomTopic: false,
    snackbar: false,
    snackMsg: "",

    ros: null,
    topic: "",
    message: "",
    listener: null,
    connected: false,
    subscriberData: false,
  }),
  mounted() {
    this.connect();
  },
  computed: {
    items: function () {
      let items = [
        {
          name: "/" + this.robot.name + "/camera_node/image/compressed",
          messageType: "sensor_msgs/CompressedImage",
        },
      ];
      return items;
    },
  },

  methods: {
    connect() {
      this.ros = new ROSLIB.Ros({
        url: this.wsAddress,
      });

      this.ros.on("connection", () => {
        this.connected = true;
      });
      this.ros.on("error", (error) => {
        console.error(error);
      });
      this.ros.on("close", () => {
       // console.log("connection closed");
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
        //this.unSubscribe();
        this.subscriberData = !!data;
      });
      this.sleep(5000).then(() => {
        if (!this.subscriberData) {
          this.snackbar = true;
          this.snackMsg = "El robot tarda demasiado en retornar una respuesta. ¿Estás segur@ que publica información en este topic?"
        }
      });
    },
    unSubscribe() {
      this.topic.unsubscribe();
    },
    addTopic() {
      if (this.customMsgType && this.customTopic) {
        this.items.push({
          name: this.customTopic,
          messageType: this.customMsgType,
        });
        this.customMsgType = "";
        this.customTopic = "";
        this.addCustomTopic = false;
      } else {
        this.snackbar = true;
        this.snackMsg = "Debes agregar la información solicitada";
      }
    },
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },
};
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
</style>