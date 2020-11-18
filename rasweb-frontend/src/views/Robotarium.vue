<template>
  <div>
    <MainVideoStream />
  </div>
</template>



<script>
import {mapMutations} from "vuex";
import MainVideoStream from "@/components/MainVideoStream.vue";
export default {
  name: "Robotarium",
  components: {
    MainVideoStream,
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
