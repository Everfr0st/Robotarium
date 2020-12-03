<template>
  <div>
    <v-skeleton-loader
      v-if="!isActive"
      class="mx-auto"
      type="card"
    ></v-skeleton-loader>
    <v-lazy
      :options="{
        threshold: 0.5,
      }"
      min-height="200"
      transition="fade-transition"
      v-if="isActive"
    >
      <v-card 
       color="#bdbdbdd7" 
      @mouseover="showActions=true;"
      @mouseleave="showActions=false">
        <v-carousel
          :continuous="false"
          hide-delimiters
          height="230"
          gradient="to top, rgba(0,0,0,.1), rgba(0,0,0,.5)"
        >
          <v-carousel-item
            v-for="(element, index) in api_data"
            :key="index"
            :src="element.photo == 'null' ? '' : element.photo"
            reverse-transition="fade-transition"
            transition="fade-transition"
          >
            <header class="card-header">
              <v-card-title>
                <h3 :title="element.code">{{ element.code }}</h3>
              </v-card-title>
              <v-card-subtitle :title="element.name" style="color: white">
                {{ element.name }}
              </v-card-subtitle>
            </header>
            <v-card-actions class="actions" v-if="showActions">
              <v-btn title="Reservar" fab color="accent" @click="showCalendar(element);">
                <v-icon>mdi-calendar-plus</v-icon>
              </v-btn>
            </v-card-actions>
          </v-carousel-item>
        </v-carousel>
      </v-card>
    </v-lazy>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import Schedule from "@/components/subcomponents/Schedule.vue";
export default {
  name: "CardInventory",
  props: ["stand", "row", "col"],
  components: {
    Schedule
  },
  data: () => ({
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    isActive: false,
    api_dir: "/robotarium-api/v1.0/item-detail/?format=json&code=",
    api_data: "",
    showActions: false
  }),
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  async created() {
    let response = await fetch(
      this.domainBase +
        this.api_dir +
        this.stand +
        "-" +
        (this.row - 1) +
        (this.col - 1),
      {
        method: "GET", // *GET, POST, PUT, DELETE, etc.
        headers: {
          Authorization: `Bearer ${this.authentication.accessToken}`,
        },
      }
    );
    response = await response.json();
    this.api_data = response;
    this.isActive = true;
  },
  methods:{
    ...mapMutations(["setReservation"]),
    showCalendar(element){
      let reservationObj = {
        element: element,
        showDialog: true,
      }
      this.setReservation(reservationObj);
    }
  }
};
</script>

<style scoped>
.actions {
  padding: 0px auto;
  position: absolute;
  bottom: 0px;
}
.card-header {
  background: rgba(0, 0, 0, 0.4);
}
</style>