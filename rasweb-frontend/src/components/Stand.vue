<template>
  <div>
    <v-container fluid>
      <v-row v-for="row in parseInt(levels)" :key="row" wrap>
        <v-col class="col-card" v-for="col in 3" cols="12" sm="12" md="4" :key="col">
          <CardInventory class="card" :stand="stand" :col="col" :row="row" />
        </v-col>
      </v-row>
    </v-container>
    <v-dialog :retain-focus="false" v-model="reservation.showDialog">
      <Schedule
        v-on:closeDatePicker="reservation.showDialog = false"
        v-if="reservation.showDialog"
        :item="reservation.element"
      />
    </v-dialog>
  </div>
</template>
<script>
import { mapState } from "vuex";
import CardInventory from "@/components/subcomponents/CardInventory.vue";
import Schedule from "@/components/subcomponents/Schedule.vue";

export default {
  name: "Stand",
  data: () => ({
    api_dir: "/robotarium-api/v1.0/inventory-list/?format=json",
    data_api: [],
  }),
  components: {
    CardInventory,
    Schedule,
  },
  computed: {
    ...mapState(["domainBase", "authentication", "reservation"]),
  },
  props: ["stand", "levels"],
};
</script>

<style scoped>
.card {
  width: 100%;
  height: auto;
  overflow: hidden;
}

</style>