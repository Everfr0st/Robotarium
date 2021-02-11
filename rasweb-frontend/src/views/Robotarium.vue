<template>
  <div>
    <v-container class="robotarium" fluid>
      <v-row>
        <v-col md="4" lg="3">
          <RobotVideoStream />
        </v-col>
        <v-col md="8" lg="9">
          <MainVideoStream />
          <tacometer />
        </v-col>
      </v-row>
    </v-container>

    <v-overlay id="overlay" opacity="0.8">
      <div class="display-1 pa-5 mt-12">
        El robotarium RAS-UAO no funciona correctamente en dispositivos con
        resoluciones menores a 1200px
      </div>
    </v-overlay>
  </div>
</template>



<script>
import { mapMutations, mapState } from "vuex";
import MainVideoStream from "@/components/MainVideoStream.vue";
import RobotVideoStream from "@/components/RobotVideoStream.vue";
import Tacometer from "../components/Tacometer.vue";
export default {
  name: "Robotarium",
  components: {
    MainVideoStream,
    RobotVideoStream,
    Tacometer,
  },
  data: () => ({
    apiDir: "/robotarium-api/v1.0/robot-status/",
  }),
  created() {
    document.title = "Robotarium Live Stream · UAO-RAS";
    this.setViewname("Robotarium");
  },
  mounted() {
    this.$root.$on("ROSconnected", (data) => {
      this.updateRobotStatus(data);
    });
  },
  computed: {
    ...mapState(["reservation", "domainBase"]),
  },
  methods: {
    ...mapMutations(["setViewname"]),
    updateRobotStatus(data) {
      fetch(this.domainBase + this.apiDir, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
    },
  },
};
</script>
<style>
@media (max-width: 1200px) {
  .robotarium {
    display: none;
  }
  #overlay {
    display: block;
  }
}
@media (min-width: 1200px) {
  #overlay {
    display: none;
  }
  .robotarium {
    display: block;
    padding: 0 15px;
  }
}
</style>
