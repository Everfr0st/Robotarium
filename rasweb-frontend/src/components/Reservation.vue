<template>
  <div>
    <v-expansion-panels accordion focusable>
      <v-expansion-panel  >
        <v-expansion-panel-header> Estante A </v-expansion-panel-header>
        <v-expansion-panel-content>
          <Stand class="pa-0" stand="A" levels="5" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel >
        <v-expansion-panel-header> Estante B </v-expansion-panel-header>
        <v-expansion-panel-content>
          <Stand class="mt-4 pa-0" stand="B" levels="6" />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
import Stand from "@/components/Stand.vue";
export default {
  name: "Reservation",
  components: {
    Stand,
  },
  created() {
    document.title = "Inventario · UAO-RAS";
  },
};
</script>

<style>
</style>