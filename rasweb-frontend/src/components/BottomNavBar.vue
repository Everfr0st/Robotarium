<template>
  <div>
    <v-bottom-navigation v-if="authentication.accessToken" grow id="bottom-nav" color="primary">
      <v-container fluid>

      <v-row align="center" justify="space-around">
        <v-col class="pa-0">
          <v-btn class="pa-2" block exact :to="{ name: 'Home' }">
            <span>Inicio</span>

            <v-icon>mdi-home</v-icon>
          </v-btn>
        </v-col>
        <v-col class="pa-0">
          <v-btn class="pa-2" block exact :to="{ name: 'Inventory' }">
            <span>Inventario</span>

            <v-icon>mdi-store</v-icon>
          </v-btn></v-col
        >
        <v-col class="pa-0">
          <v-btn class="pa-2" block exact :to="{ name: 'Robotarium' }">
            <span>Robotarium</span>

            <v-icon>mdi-robot</v-icon>
          </v-btn></v-col
        >
      </v-row>
            </v-container>

    </v-bottom-navigation>
  </div>
</template>

<script>
import {mapState} from "vuex";
export default {
  name: "BottomNavBar",
  computed:{
    ...mapState(["authentication"])
  }
};
</script>

<style>
@media (max-width: 1264px) {
  #bottom-nav {
    display: block;
    position: fixed;
    bottom: 0%;
    z-index: 100;
    max-width: 100%;
  }
}
@media (min-width: 1264px) {
  #bottom-nav {
    display: none;
  }
}
</style>