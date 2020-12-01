<template>
  <div>
    <v-card class="pa-3">
      <v-autocomplete
                    v-model="robot"
                    :items="robots"
                    chips
                    color="accent lighten-2"
                    label="Selecciona un robot"
                    item-text="name"
                    item-value="name"
                    
                  >
                    <template v-slot:selection="data">
                        
                      <v-chip
                        v-bind="data.attrs"
                        :input-value="data.selected"
                                              >
                        <v-avatar left v-if="data.item.photo">
                          <img
                            :src="data.item.photo"
                            :alt="data.item.name"
                          />
                        </v-avatar>
                        <v-avatar left color="secondary" v-else>
                          <span
                            v-if="!data.item.photo"
                            style="color: white; font-size: 8pt"
                            >{{data.item.name.slice(0,1)}}</span
                          >
                        </v-avatar>
                        {{
                          data.item.name
                        }}
                      </v-chip>
                    </template>
                    <template v-slot:item="data">
                      <template v-if="typeof data.item !== 'object'">
                        <v-list-item-content
                          v-text="data.item"
                        ></v-list-item-content>
                      </template>
                      <template v-else>
                        <v-list-item-avatar
                          left
                          color="secondary white--text"
                        >
                          <img
                          v-if="data.item.photo"
                            :src="data.item.photo"
                            :alt="data.item.name"
                          />
                          <span v-else>
                              {{data.item.name.slice(0,1)}}
                          </span>

                        </v-list-item-avatar>

                        <v-list-item-content>
                          <v-list-item-title
                            v-html="data.item.name"
                          ></v-list-item-title>
                          <v-list-item-subtitle
                            v-html="data.item.available? 'Disponible':'No disponible'"
                          ></v-list-item-subtitle>
                        </v-list-item-content>
                      </template>
                    </template>
                  </v-autocomplete>
      <WebSocketLive number="" />
    </v-card>
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
    robot: ''
  }),
  components: {
    WebSocketLive,
  },
  created() {
    let robotariumInfo = {
      robot: "Duckiebot1",
    };
    this.setRobotariumInfo(robotariumInfo);
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
        .then((response) =>{
            
            this.robots = response
        }
        )
        .catch(() => {}); //Hacer algo al error en respuesta
    },
  },
};
</script>