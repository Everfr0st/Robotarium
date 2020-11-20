<template>
  <div>
    <v-card class="pa-0 ma-0">
      <v-date-picker
        v-model="date"
        :min="startDate"
        :max="EndDate"
        full-width
        style="position: relative"
        @change="setActive();"
      >
        <v-btn @click="reserve()" v-if="active" class="new-scheduler" fab dark color="accent">
          <v-icon dark> mdi-plus </v-icon>
        </v-btn>
      </v-date-picker>
    </v-card>
    <v-dialog  max-width="500px" v-model="showDialog">
      <HourReserve v-if="showDialog" :date="date" :item="item"/>
    </v-dialog>
  </div>
</template>

<script>
import HourReserve from "@/components/subcomponents/HourReserve.vue";
export default {
  name: "Schedule",
  components:{
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
      let select_date = this.date.split("-");
      let selectDate = new Date(select_date[0], select_date[1], select_date[2]);
      if (selectDate.getDay() == 1 || selectDate.getDay() == 2) {
        this.active = false;
      } else {
        this.active = true;
      }
    },
    reserve(){
      this.showDialog = true;
    }
  },
};
</script>

<style scoped>
.new-scheduler {
  position: absolute;
  right: 5%;
  bottom: 10px;
}
</style>