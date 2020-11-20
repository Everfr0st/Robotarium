<template>
  <div class="ml-4">
    <h3>Vitrina {{ stand }}</h3>
    <v-container class="pa-0">
      <v-row v-for="row in parseInt(levels)" :key="row">
        <v-col v-for="col in 3" :key="col" class="item-card">
          <CardInventory class="card" :stand="stand" :col="col" :row="row" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import { mapState } from "vuex";
import CardInventory from "@/components/subcomponents/CardInventory.vue";
export default {
  name: "Stand",
  data: () => ({
    api_dir: "/robotarium-api/v1.0/inventory-list/?format=json",
    data_api: [],
  }),
  components: {
    CardInventory,
  },
  computed: {
    ...mapState(["domain_base", "authentication"]),
  },
  props: ["stand", "levels"],
  created() {
    /* let response = await fetch(
      this.domain_base + this.api_dir + "&code=" + this.stand,
      {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        headers: {
          Authorization: `Bearer ${this.authentication.accessToken}`,
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
.item-card {
  max-width: 33%;
}
</style>