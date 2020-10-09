<template>
  <v-app>
    <NavBar />
    <v-main>
      <v-container fluid>
        <v-row wrap>
          <v-col sm="6" md="3" color="primary">
            <LeftAside/>
          </v-col>
          <v-col md="6" color="red">
            2
          </v-col>
          <v-col md="3" color="green">
            <RightAside/>
          </v-col>
        </v-row>
        
      </v-container>
    </v-main>
  </v-app>
</template>

<script>



import LeftAside from "@/components/LeftAside.vue";
import RightAside from "@/components/RightAside.vue";
import NavBar from "@/components/NavBar.vue";



export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    RightAside
  },

  data: () => ({
    //
  }),
};
</script>
