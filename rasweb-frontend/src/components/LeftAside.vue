<template>
  <div>
    <v-container wrap>
      <v-row
         justify="left"
        v-for="(item, index) in elements"
        :key="index"
        wrap
      >
        <v-btn
        align="left"
          color="primary secondary--text"
          class="ma-2"
          text
          :to="{ name: item.link }"
          exact
          rounded
        >
          <v-icon left>{{ item.icon }}</v-icon>
          <h3>
            {{ item.title }}
          </h3>
        </v-btn>
      </v-row>
    </v-container>
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