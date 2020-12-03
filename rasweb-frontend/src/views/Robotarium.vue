<template>
  <div>
    <MainVideoStream />
    <RobotVideoStream />
    
  </div>
</template>



<script>
import {mapMutations, mapState} from "vuex";
import MainVideoStream from "@/components/MainVideoStream.vue";
import RobotVideoStream from "@/components/RobotVideoStream.vue";
import HourReserve from "@/components/subcomponents/HourReserve.vue";
export default {
  name: "Robotarium",
  components: {
    MainVideoStream,
    RobotVideoStream,
    HourReserve
  },
  created() {
    document.title = "Robotarium Live Stream · UAO-RAS";
    this.setViewname("Robotarium")
  },
  computed:{
    ...mapState(["reservation"])
  },
  methods:{
    ...mapMutations(["setViewname"])
  }
};
</script>
