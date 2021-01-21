<template>
  <div>
    <v-bottom-navigation grow id="bottom-nav" color="primary">
      <v-row class="px-3 pt-0">
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
    </v-bottom-navigation>
  </div>
</template>

<script>
export default {};
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