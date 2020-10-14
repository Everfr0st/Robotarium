<template>
  <div>
    <v-layout wrap>
      <v-flex v-for="(item, index) in elements" :key="index">
        <v-btn
          color="primary secondary--text"
          class="ma-2"
          text
          block
          elevation="2"
          :to="{ name: item.link }"
          exact
          rounded
        >
          <v-row  class="pa-4">
            <h2>
<v-icon left>{{ item.icon }}</v-icon>
              {{ item.title }}   
            </h2>
                
          </v-row>
        </v-btn>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: "LeftAside",
  data: () => ({
    elements: [
      {
        title: "Inicio",
        icon: "mdi-home",
        link: "Home",
      },
      {
        title: "Inventario",
        icon: "mdi-store",
        link: "Inventory",
      },
      {
        title: "Robotarium",
        icon: "mdi-robot",
        link: "Robotarium",
      },
    ],
  }),
};
</script>

<style scoped>
.btn-menu {
  background-color: rgba(190, 7, 7, 0.4);
}
</style>