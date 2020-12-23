<template>
  <div>
    <v-tabs v-model="tab" class="mt-1">
      <v-tab> <v-icon left>mdi-calendar-multiple</v-icon> Reservar </v-tab>
      <v-tab><v-icon left>mdi-text-box-search</v-icon> Historial</v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <div>
          <Reservation class="mt-3" />
        </div>
      </v-tab-item>
      <v-tab-item
        ><div>
          <History class="mt-3" />
        </div>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import Reservation from "@/components/Reservation.vue";
import History from "@/components/History.vue";
import { mapMutations } from "vuex";
export default {
  name: "Inventory",
  data: () => ({
    tab: "",
  }),
  components: {
    Reservation,
    History,
  },
  created() {
    this.setViewname("Inventario");
  },
  methods: {
    ...mapMutations(["setViewname"]),
  },
};
</script>