<template>
  <div>
    <v-container wrap>
      <v-row>
        <h3 class="ml-3" style="padding-top: 5px" align-center>Usuarios</h3>
        <v-spacer></v-spacer>
        <v-btn fab text small color="grey" class="mr-3">
          <v-icon>mdi-home</v-icon>
        </v-btn>
      </v-row>
      <v-row wrap>
        <v-col class="pa-0">
          <v-skeleton-loader
            
            v-bind="attrs"
            type="list-item-avatar"
          ></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "RightAside",
  data: () => ({
      attrs: {
        boilerplate: false,
      },

  }),
};
</script>

<style scoped>
.btn-menu {
  background-color: rgba(190, 7, 7, 0.4);
}
</style>