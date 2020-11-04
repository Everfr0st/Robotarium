<template>
  <div>
      <v-row class="pa-2">

      <v-icon left color="primary">mdi-access-point</v-icon><h3 >Robotarium</h3>
      </v-row>
    <iframe
      class="skeleton"
      width="100%"
      height="400"
      :src="'https://www.youtube.com/embed/' + liveId"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
    ></iframe>
  </div>
</template>
<script>
import { mapState } from "vuex";
export default {
  data: () => ({
    liveId: "",
    api_dir: "/coco-api/v1.0/retrieve-liveId/",
  }),
  computed: {
    ...mapState(["domain_base", "authentication"]),
  },
  async created() {
    let options = {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Bearer ${this.authentication.accessToken}`,
      },
    };
    let response = await fetch(this.domain_base + this.api_dir, options);
    response = await response.json();
    this.liveId = response.live_id;
  }
    
}
</script>

<style scoped>
  .skeleton {
  background: linear-gradient(90deg, #ededed, #ffffff, #ededed);
  animation-name: load;
  animation-duration: 1.5s;
  animation-iteration-count: infinite;
  animation-direction: forwards;
  animation-timing-function: ease;
  background-size: 150% 100%;
}
@keyframes load {
  from {
    background-position: 100% 0%;
  }
  to {
    background-position: -100% 0%;
  }
}

</style>