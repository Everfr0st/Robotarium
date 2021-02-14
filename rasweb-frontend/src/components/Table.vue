<template>
  <div>
    <v-skeleton-loader
      v-if="!isActive"
      class="mx-auto"
      type="image"
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
        @mouseover="showActions = true"
        @mouseleave="showActions = false"
      >
        <v-carousel
          class="carousel"
          continuous
          hide-delimiters
          gradient="to top, rgba(0,0,0,.1), rgba(0,0,0,.5)"
          progress
          cycle
          color="accent"
          height="340"
        >
          <v-carousel-item
            v-for="(element, index) in apiData"
            :key="index"
            :src="element.photo == 'null' ? '' : element.photo"
            reverse-transition="fade-transition"
            transition="fade-transition"
          >
            <header class="card-header ">
              <v-card-title>
                <h3 :title="element.code">{{ element.code }}</h3>
              </v-card-title>
              <v-card-subtitle :title="element.name" class="white--text">
                {{ element.name }}
              </v-card-subtitle>
            </header>
            <v-card-actions class="actions" v-if="showActions">
              <v-btn
                title="Reservar"
                fab
                color="accent"
                @click="showCalendar(element)"
              >
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
  props: ["position", "level"],
  components: {
    Schedule,
  },
  data: () => ({
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    isActive: false,
    apiDir: "/robotarium-api/v1.0/item-detail/?format=json&code=",
    apiData: "",
    showActions: false,
  }),
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  async created() {
    let response = await fetch(
      this.domainBase +
        this.apiDir +
        "M-" +
        (this.position - 1) +
        (this.level - 1),
      {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      }
    );
    response = await response.json();
    this.apiData = response;
    this.isActive = true;
  },
  methods: {
    ...mapMutations(["setReservation"]),
    showCalendar(element) {
      let reservationObj = {
        element: element,
        showDialog: true,
      };
      this.setReservation(reservationObj);
    },
  },
};
</script>

<style>
.card-header {
  background: rgba(0, 0, 0, 0.4);
}
.actions {
  padding: 0px auto;
  position: absolute;
  bottom: 0px;
}
</style>