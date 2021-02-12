<template>
  <div>
    <v-container fluid>
      <v-row v-for="row in parseInt(levels)" :key="row" wrap>
        <v-col class="col-card" v-for="col in 3" sm="6" md="4" :key="col">
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
  created() {
    /* let response = await fetch(
      this.domainBase + this.api_dir + "&code=" + this.stand,
      {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      }
    );
    response = await response.json();
    let aux_array = [];
    for (let index = 0; index < response.length; index++) {
      if (index == 0) {
        aux_array.push(response[index]);
      } else {
        let current_obj_array = response[index].code.split("-")[1].split("");
        let previous_obj_array = response[index - 1].code
          .split("-")[1]
          .split("");
        if (current_obj_array[0] == previous_obj_array[0]) {
          aux_array.push(response[index]);
        } else {
          this.data_api.push(aux_array);
          console.log(aux_array);
          aux_array = [];
        }
      }
    }*/
  },
};
</script>

<style scoped>
.card {
  width: 100%;
  height: auto;
  overflow: hidden;
}
@media (max-width: 600px) {
  .col-card {
    min-width: 94vw;
  }
  .card {
    height: 100%;
  }
}
</style>