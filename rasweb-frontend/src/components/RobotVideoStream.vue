<template>
  <div>
    <v-card class="pa-3 mr-4">
      <v-autocomplete
        v-model="robot"
        :items="robots"
        chips
        color="accent"
        label="Selecciona un robot"
        item-text="name"
        item-value="name, available"
        :readonly="showRobotTools"
      >
        <template v-slot:selection="data">
          <v-chip v-bind="data.attrs" :input-value="data.selected">
            <v-badge
              bottom
              overlap
              dot
              offset-x="13px"
              offset-y="8px"
              :color="data.item.available ? 'green' : 'grey'"
            >
              <v-avatar color="secondary" left>
                <img
                  :src="data.item.photo"
                  :alt="data.item.name"
                  v-if="data.item.photo"
                />
                <span v-else style="color: white; font-size: 8pt">{{
                  data.item.name.slice(0, 1)
                }}</span>
              </v-avatar>
            </v-badge>
            {{ data.item.name }}
          </v-chip>
        </template>
        <template v-slot:item="data">
          <template v-if="typeof data.item !== 'object'">
            <v-list-item-content v-text="data.item"></v-list-item-content>
          </template>
          <template v-else>
            <v-badge
              bottom
              overlap
              dot
              offset-x="0px"
              offset-y="23px"
              :color="data.item.available ? 'green' : 'grey'"
            >
              <v-list-item-avatar
                @click="setRobotInfo(data.item)"
                color="secondary"
              >
                <img
                  :src="data.item.photo"
                  :alt="data.item.name"
                  v-if="data.item.photo"
                />
                <span v-else style="color: white; font-size: 8pt">{{
                  data.item.name.slice(0, 1)
                }}</span>
              </v-list-item-avatar>
            </v-badge>

            <v-list-item-content @click="setRobotInfo(data.item)">
              <v-list-item-title v-html="data.item.name"></v-list-item-title>
              <v-list-item-subtitle
                class="ml-3"
                v-html="data.item.available ? 'Disponible' : ' No disponible'"
              ></v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </template>
      </v-autocomplete>
      <v-card-actions v-if="robot">
        <v-btn @click="closeRobotTools" :color="showRobotTools? '' : 'error'">
          {{ showRobotTools? "" : "Desconectar" }}
        </v-btn>
      </v-card-actions>
    </v-card>
    <div v-if="robot">
      <v-card class="mt-3 mr-4">
        <joistick :wsAddress="'ws://0.0.0.0:' + getMeta.websocket" />
      </v-card>
      <v-card class="mt-4 px-3 mr-4 pb-3">
        <robot-image
          :wsAddress="'ws://0.0.0.0:' + getMeta.websocket"
          v-on:robotView="setRobotImage"
        />
      </v-card>

      <v-card
        elevation="3"
        width="400"
        :height="img ? '260' : '200'"
        id="drag-box"
      >
        <v-skeleton-loader
          v-if="!img"
          class="mx-auto"
          max-width="400"
          min-height="400"
          type="image"
        >
        </v-skeleton-loader>

        <img v-else :src="'data:image/png;base64,' + img" />
      </v-card>
    </div>

    <v-snackbar v-model="snackbar">
      {{ message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template> 

<script>
import { mapState, mapMutations } from "vuex";
import WebSocketLive from "@/components/subcomponents/WebSocketLive.vue";
import Joistick from "../components/Joistick.vue";
import RobotImage from "../components/RobotImage.vue";
export default {
  name: "RobotVideoStream",
  data: () => ({
    robots: [],
    apiDir: "/robotarium-api/v1.0/robot-list/?format=json",
    robot: "",
    robotObj: "",
    imgBox: false,
    robotAvailable: false,
    showRobotTools: false,
    dragEvent: "",
    snackbar: false,
    message: "",
    img: "",
  }),
  components: {
    WebSocketLive,
    Joistick,
    RobotImage,
  },
  created() {
    this.getApiInfo();
  },
  computed: {
    ...mapState(["domainBase", "authentication"]),
    getMeta: function () {
      return JSON.parse(this.robotObj.meta);
    },
  },
  methods: {
    ...mapMutations(["setRobotariumInfo"]),
    getApiInfo() {
      fetch(this.domainBase + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            throw new Error();
          }
        })
        .then((response) => {
          this.robots = response;
          console.log(response);
        })
        .catch(() => {}); //Hacer algo al error en respuesta
    },
    setRobotInfo(info) {
      this.robotObj = info;
    },
    closeRobotTools() {
      this.robot = "";
      this.showRobotTools = false;
      this.imgBox = false;
      this.img = "";
    },
    dragElement() {
      var elmnt = document.getElementById("drag-box");
      elmnt.style = "display: block;";
      var pos1 = 0,
        pos2 = 0,
        pos3 = 0,
        pos4 = 0;
      if (document.getElementById(elmnt.id + "header")) {
        // if present, the header is where you move the DIV from:
        document.getElementById(
          elmnt.id + "header"
        ).onmousedown = dragMouseDown;
      } else {
        // otherwise, move the DIV from anywhere inside the DIV:
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }

      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:

        elmnt.style.top = elmnt.offsetTop - pos2 + "px";
        elmnt.style.left = elmnt.offsetLeft - pos1 + "px";
      }

      function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
      }
    },
    setRobotImage(data) {
      if (data) this.img = data;
      if (!this.imgBox) {
        this.dragElement();
        this.imgBox = true;
      }
    },
  },
};
</script>

<style scoped>
#drag-box {
  position: fixed;
  bottom: 3%;
  right: 1%;
  max-width: 400px;
  max-height: 260px;
  cursor: pointer;
  border-radius: 10px;
  overflow: hidden;
  z-index: 100;
}
#drag-box img {
  height: 260px;
  max-width: 100%;
}
.chip {
  position: absolute;
  z-index: 101;
  right: 5px;
  top: 3px;
}
</style>