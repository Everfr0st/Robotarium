<template>
  <v-app>
    <NavBar />
    <v-main>
      <v-container fluid>
        <v-row wrap>
          <v-col sm="6" md="3" color="primary">
            <LeftAside/>
          </v-col>
          <v-col sm="12" md="6" color="red">
            <router-view/>
          </v-col>
          <v-col class="pa-0" sm="12" md="3" lg="3" color="green">
            <RightAside/>
          </v-col>
        </v-row>
        <UserDetailDialog/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>



import LeftAside from "@/components/LeftAside.vue";
import RightAside from "@/components/RightAside.vue";
import NavBar from "@/components/NavBar.vue";
import UserDetailDialog from "@/components/UserDetailDialog.vue";



export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    RightAside,
    UserDetailDialog
  },

  data: () => ({
    //
  }),
};
</script>
