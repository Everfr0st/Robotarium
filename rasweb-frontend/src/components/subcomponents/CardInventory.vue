<template>
  <div>
       <v-skeleton-loader
    v-if="!isActive"
      class="mx-auto"
      max-width="300"
      type="card"
    ></v-skeleton-loader>
    <v-lazy
       v-model="isActive"
      :options="{
        threshold: 0.5,
      }"
      min-height="200"
      transition="fade-transition"
    >
      <v-card elevation="3">
        <v-carousel
          :continuous="false"
          :cycle="cycle"
          hide-delimiter-background
          height="230"
          v-model="model"
          gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
        >
          <v-carousel-item v-for="(color, i) in colors" :key="color">
            <v-sheet :color="color" height="100%" tile>
              <v-row align="center" justify="center">
                <h4>{{ stand }}-{{ row - 1 }}{{ col - 1 }}{{ i }}</h4>
              </v-row>
            </v-sheet>
          </v-carousel-item>
        </v-carousel>
      </v-card>
    </v-lazy>
   
  </div>
</template>

<script>
export default {
  name: "CardInventory",
  props: ["stand", "row", "col"],
  data: () => ({
    model: 0,
    colors: ["primary", "secondary", "yellow darken-2", "red", "orange"],
    isActive: '',
  }),
};
</script>