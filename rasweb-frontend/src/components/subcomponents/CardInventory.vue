<template>
  <div>
    <v-skeleton-loader
      v-if="!isActive"
      class="mx-auto"
      max-width="300"
      type="card"
    ></v-skeleton-loader>
    <v-lazy
      :options="{
        threshold: 0.5,
      }"
      min-height="200"
      transition="fade-transition"
    >
      <v-card  color="#979797f5">
        <v-carousel
          :continuous="false"
          hide-delimiters
          height="230"
          gradient="to top, rgba(0,0,0,.1), rgba(0,0,0,.5)"
        >
          <v-carousel-item
            v-for="(element, index) in api_data"
            :key="index"
            :src="element.photo == 'null' ? '': element.photo"
            reverse-transition="fade-transition"
            transition="fade-transition"
            max-width= "230"
          >
          <header class="card-header">
              <v-card-title>
              <h3>{{element.code}}</h3>
            </v-card-title>
            <v-card-subtitle style="color: white;" >
              {{ element.name }} 
            </v-card-subtitle>
          </header>
            <v-card-actions class="actions">
              <v-btn elevation="1" outlined color="primary">
                Reservar
              </v-btn>
            </v-card-actions>
          </v-carousel-item>
        </v-carousel>
      </v-card>
    </v-lazy>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "CardInventory",
  props: ["stand", "row", "col"],
  data: () => ({
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    isActive: false,
    api_dir: "/robotarium-api/v1.0/item-detail/?format=json&code=",
    api_data: "",
  }),
  computed: {
    ...mapState(["domain_base", "authentication"]),
  },
  async created() {
    let response = await fetch(
      this.domain_base +
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
};
</script>

<style scoped>
    .actions{
        
        position: absolute;
        bottom: 0px;
    }
    .card-header{
        background: rgba(0,0,0,0.4);
    }
</style>