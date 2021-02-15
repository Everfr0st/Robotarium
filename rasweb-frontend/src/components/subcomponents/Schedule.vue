<template>
  <div>
    <v-card>
      <v-date-picker
        v-model="date"
        :min="startDate"
        full-width
        style="position: relative"
        @change="setActive()"
        range
        width="600"
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
      <v-btn
        @click="reserve()"
        v-if="allDay"
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
        :date="date[0]"
        :item="item"
      />
    </v-dialog>
    <v-snackbar v-model="snackbar" timeout="5000">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" outlined v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
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
    date: [],
    startDate: new Date().toISOString().slice(0, 10),
    active: true,
    showDialog: false,
    allDay: false,
    snackbar: false,
    message: "",
  }),
  watch: {
    date() {
      if (this.date.length > 1) {
        let endDate = this.str2Date(this.date[1].split("-"));
        let startDate = this.str2Date(this.date[0].split("-"));
        if (startDate - endDate > 0) {
          this.date.unshift(this.date[1]);
          this.date.pop();
        } else if (startDate - endDate == 0) {
          this.date.pop();
        }
      }
      this.setActive();
    },
  },
  methods: {
    setActive() {
      this.active = false;
      if (this.date.length > 1) {
        this.active = true;
        let weekDayStart = this.getWeekDay(this.date[0]);
        let weekDayEnd = this.getWeekDay(this.date[1]);
        if (weekDayStart < 6 && weekDayEnd < 6) {
          this.active = true;
        } else {
          this.active = false;
          this.snackMsg();
        }
      } else if (this.date.length == 1) {
        let weekDay = this.getWeekDay(this.date[0]);
        if (weekDay == 6 || weekDay == 7) {
          this.active = false;
          this.snackMsg();
        } else {
          this.active = true;
        }
      }
    },
    getWeekDay(date) {
      let dateDay = new Date(date).getDay() + 1;
      return dateDay;
    },
    reserve() {
      this.showDialog = true;
    },
    str2Date(dateStr) {
      var date = new Date(dateStr[0], dateStr[1], dateStr[2]);
      return date.getTime();
    },
    snackMsg() {
      if (!this.active) {
        this.snackbar = true;
        this.message =
          "Las fechas de inicio y final no pueden ser en fin de semana.";
      }
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