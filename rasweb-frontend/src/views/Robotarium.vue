<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col md="4" lg="3">
          <RobotVideoStream />
          
        </v-col>
        <v-col md="8" lg="9">
          <MainVideoStream />
        </v-col>
      </v-row>
    </v-container>

    
  </div>
</template>



<script>
import { mapMutations, mapState } from "vuex";
import MainVideoStream from "@/components/MainVideoStream.vue";
import RobotVideoStream from "@/components/RobotVideoStream.vue";

export default {
  name: "Robotarium",
  components: {
    MainVideoStream,
    RobotVideoStream,
  },
  created() {
    document.title = "Robotarium Live Stream · UAO-RAS";
    this.setViewname("Robotarium");
  },
  computed: {
    ...mapState(["reservation"]),
  },
  methods: {
    ...mapMutations(["setViewname"]),
  },
};
</script>
