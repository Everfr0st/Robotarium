<template>
  <div>
    <v-container class="pt-4 white" >
      <v-row class="white"  v-for="(item, index) in elements" :key="index" wrap>
        <v-btn
          small
          align="left"
          active-class="primary lighthen-10"
          class="ma-2"
          text
          :to="{ name: item.link }"
          exact
          rounded
        >
          <v-icon left small>{{ item.icon }}</v-icon>
          <h3>
            {{ item.title }}
          </h3>
        </v-btn>
      </v-row>
      <v-row class="white" wrap>
        <v-btn
          small
          align="left"
          active-class="primary lighthen-10"
          class="ma-2"
          text
          href="http://uaoras.tonohost.com/"
          target="_blank"
          exact
          rounded
        >
          <v-icon left small>mdi-text-box-multiple</v-icon>
          <h3>
            RAS
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
  background-color: rgba(190, 7, 7, 0.123);
}
.primary--text {
  color: black;
}
</style>