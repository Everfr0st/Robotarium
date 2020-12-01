<template>
  <div>
    <v-card class="pa-3 mr-3">
      <v-autocomplete
        v-model="robot"
        :items="robots"
        chips
        color="accent lighten-2"
        label="Selecciona un robot"
        item-text="name"
        item-value="name, available"
        :readonly="robotStream"
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
      <p v-if="robotObj.available && robot">
          Envíale información al robot {{robotObj.name}} a través de la dirección ip <strong>{{robotObj.ip}} </strong> 
      </p>
      <v-card-actions class="ma-0 pa-0">
        <v-btn
          :disabled="!robotObj.available"
          @click="showRobotStreaming"
          :color="robotStream ? 'error' : 'accent'"
          >{{ robotStream ? "Cerrar" : "Vista del robot" }}</v-btn
        >
      </v-card-actions>
    </v-card>
    
    <v-card elevation="3" id="drag-box">
      <v-chip
        v-if="robotStream"
        class="chip"
        close
        color="primary"
        @click="showRobotStreaming"
        @click:close="showRobotStreaming"
      >
        Cerrar
      </v-chip>
      <WebSocketLive number="" :robot="true" v-if="robotStream" />
    </v-card>
    <v-snackbar v-model="snackbar">
      {{ message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template> 

<script>
import { mapState, mapMutations } from "vuex";
import WebSocketLive from "@/components/subcomponents/WebSocketLive.vue";
export default {
  name: "RobotVideoStream",
  data: () => ({
    robots: [],
    apiDir: "/robotarium-api/v1.0/robot-list/?format=json",
    robot: "",
    robotObj: "",
    robotAvailable: false,
    robotStream: false,
    dragEvent: "",
    snackbar: false,
    message: "",
  }),
  components: {
    WebSocketLive,
  },
  created() {
    this.getApiInfo();
  },
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  methods: {
    ...mapMutations(["setRobotariumInfo"]),
    getApiInfo() {
      fetch(this.domainBase + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${this.authentication.accessToken}`,
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
        })
        .catch(() => {}); //Hacer algo al error en respuesta
    },
    setRobotInfo(info) {
      this.robotObj = info;
    },
    showRobotStreaming() {
      if (this.robot) {
        this.robotStream = !this.robotStream;
        if (this.robotStream) {
          this.dragElement();
          let robotariumInfo = {
            robot: this.robot,
          };
          this.setRobotariumInfo(robotariumInfo);
        } else {
          document.getElementById("drag-box").style = "display: none;";
        }
      } else {
        this.snackbar = true;
        this.message = "Debes seleccionar un robot disponible!";
      }
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
  },
};
</script>

<style scoped>
#drag-box {
  position: fixed;
  bottom: 1.5%;
  right: 1%;
  width: 300px;
  height: 200px;
  z-index: 100;
  cursor: pointer;
  display: none;
  border-radius: 5px;
  overflow: hidden;
}
.chip {
  position: absolute;
  z-index: 101;
  right: 5px;
  top: 3px;
}
</style>