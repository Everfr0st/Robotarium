<template>
  <div>
    <v-card class="pa-0 ma-0">
      <v-date-picker
        v-model="date"
        :min="startDate"
        :max="EndDate"
        full-width
        style="position: relative"
        @change="setActive()"
      >
      </v-date-picker>
      <v-btn
        title="Cerrar"
        color="white"
        class="close"
        icon
        @click="$emit('closeDatePicker')"
        ><v-icon>mdi-close</v-icon></v-btn
      >
      <v-btn
        @click="reserve()"
        v-if="active"
        class="new-scheduler"
        fab
        dark
        color="accent"
      >
        <v-icon dark> mdi-plus </v-icon>
      </v-btn>
    </v-card>
    <v-dialog :retain-focus="false" max-width="500px" v-model="showDialog">
      <HourReserve
        v-on:closeHourPicker="showDialog = false"
        v-if="showDialog"
        :date="date"
        :item="item"
      />
    </v-dialog>
  </div>
</template>

<script>
import HourReserve from "@/components/subcomponents/HourReserve.vue";

export default {
  name: "Schedule",
  components: {
    HourReserve,
  },
  props: ["item"],
  data: () => ({
    date: new Date().toISOString().slice(0, 10),
    EndDate: "",
    startDate: new Date().toISOString().slice(0, 10),
    active: true,
    showDialog: false,
  }),

  created() {
    this.getEndDate();
  },
  methods: {
    getEndDate() {
      let current_date = this.date.split("-");
      var endDate = new Date(
        current_date[0],
        (parseInt(current_date[1]) - 1).toString(),
        (parseInt(current_date[2]) + 14).toString()
      );
      this.EndDate = endDate.toISOString().substring(0, 10);
    },
    setActive() {
      let date = new Date(this.date).getDay() + 1;
      if (date == 6 || date == 7) {
        this.active = false;
      } else {
        this.active = true;
      }
    },
    reserve() {
      this.showDialog = true;
    },
  },
};
</script>

<style scoped>
.new-scheduler {
  position: absolute;
  right: 5%;
  bottom: 10px;
}
.close {
  position: absolute;
  top: 10px;
  right: 20px;
}
</style>