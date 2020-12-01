<template>
  <div>
    <MainVideoStream />
    <RobotVideoStream />
  </div>
</template>



<script>
import {mapMutations} from "vuex";
import MainVideoStream from "@/components/MainVideoStream.vue";
import RobotVideoStream from "@/components/RobotVideoStream.vue";
export default {
  name: "Robotarium",
  components: {
    MainVideoStream,
    RobotVideoStream
  },
  created() {
    document.title = "Robotarium Live Stream · UAO-RAS";
    this.setViewname("Robotarium")
  },

  methods:{
    ...mapMutations(["setViewname"])
  }
};
</script>
