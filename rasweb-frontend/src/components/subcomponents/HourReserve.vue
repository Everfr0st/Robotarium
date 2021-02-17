<template>
  <div>
    <v-card>
      <v-card-title> Habilitado: de 8am - 12m y 2pm - 6pm</v-card-title>
      <v-sheet height="500" style="overflow: hidden">
        <v-calendar
          ref="calendar"
          v-model="dateReservation"
          first-time="06:00"
          :event-more="true"
          color="primary"
          type="day"
          event-overlap-mode="stack"
          :events="events"
          :event-color="getEventColor"
          @mousedown:event="startDrag"
          @mousedown:time="startTime"
          @mousemove:time="mouseMove"
          @mouseup:time="endDrag"
        >
          <template v-slot:event="{ event, timed, eventSummary }">
            <v-container fluid>
              <v-row
                :title="!event.valid ? 'Ajusta tu franja horaria' : ''"
                class="ma-1"
              >
                <v-icon v-if="!event.valid" class="ml-3" color="error"
                  >mdi-alert</v-icon
                >
                <div class="v-event-draggable" v-html="eventSummary()"></div>
              </v-row>
            </v-container>

            <div
              v-if="timed"
              :class="
                !event.request && !reservation_created
                  ? 'v-event-drag-bottom pt-3'
                  : 'pt-3'
              "
              @mousedown.stop="extendBottom(event)"
            ></div>
          </template>
        </v-calendar>
        <v-card-actions>
          <v-btn
            title="Cerrar"
            color="error"
            class="close"
            icon
            @click="$emit('closeHourPicker')"
            ><v-icon>mdi-close</v-icon></v-btn
          >
          <v-speed-dial
            v-model="fab"
            :bottom="true"
            :right="true"
            :open-on-hover="!reservation_created"
            transition="slide-y-reverse-transition"
            class="submit-reserve"
            v-if="!disabled && !reservation_created"
          >
            <template v-slot:activator>
              <v-btn
                v-model="fab"
                dark
                fab
                :loading="loading"
                :color="reservation_created ? 'success' : 'accent'"
              >
                <v-icon v-if="fab"> mdi-close </v-icon>
                <v-icon v-else> mdi-calendar </v-icon>
              </v-btn>
            </template>
            <v-btn  @click="quantityDialog=!quantityDialog;" fab dark small color="indigo">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn @click="submitReserve()" fab dark small color="green">
              <v-icon>mdi-check</v-icon>
            </v-btn>
            <v-btn @click="removeEvent" fab dark small color="red">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-speed-dial>
        </v-card-actions>
      </v-sheet>
    </v-card>
    <v-dialog width="600" persistent v-model="quantityDialog">
      <v-card class="pa-6">
        <v-card-text>
          <v-text-field :rules="[validQuantity]"  label="Cantidad" type="number" v-model="quantity"></v-text-field>
          <v-row class="px-3">
            <v-btn :disabled="quantityBtn" @click="quantityDialog=false;" color="accent darken-2">Aceptar</v-btn>
          </v-row>
        </v-card-text>
      </v-card>
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
import { mapState } from "vuex";
export default {
  name: "HourReserve",
  props: ["date", "item"],
  data: () => ({
    value: "",
    events: [],
    selfUserEvents: [],
    colors: [
      "#8E24AA",
      "#3949AB",
      "#01579B",
      "#01579B",
      "#FB8C00",
      "#6D4C41",
      "#37474F",
      "#616161",
    ],
    dragEvent: null,
    dragStart: null,
    createEvent: null,
    createStart: null,
    extendOriginal: null,
    reserveDate: "",
    snackbar: false,
    valid: true,
    message: "",
    api_dir: "/robotarium-api/v1.0/reserve-list/",
    api_post: "/robotarium-api/v1.0/create-reservation/",
    apiResponse: [],
    index: null,
    loading: false,
    disabled: true,
    reserveSubmit: "",
    reservation_created: false,
    quantity: 1,
    fab: "",
    quantityDialog: false,
    quantityBtn: false,
     
  }),

  async created() {
    const response = await this.getApiInfo();
    this.getEvents(response);
  },
  
  computed: {
    ...mapState(["selfUser", "domainBase", "authentication"]),
    dateReservation() {
      return this.date[0];
    },
    validQuantity(){
      if(this.quantity > this.item.quantity || this.quantity < 1){
        this.quantityBtn = true;
        return `Cantidad inválida (max. ${this.item.quantity}).`
      } else{
        this.quantityBtn = false;
        return true;
      }
    }
     
  },
  methods: {
    startDrag({ event, timed }) {
      if (event && timed && !event.request) {
        this.dragEvent = event;
        this.dragTime = null;
        this.extendOriginal = null;
      }
    },
    startTime(tms) {
      const mouse = this.toTime(tms);
      if (this.dragEvent && this.dragTime === null) {
        const start = this.dragEvent.start;

        this.dragTime = mouse - start;
      } else if (this.selfUserEvents.length < 1) {
        this.createStart = this.roundTime(mouse);
        this.createEvent = {
          name: `${this.selfUser.name} separa el elemento: ${this.item.name}`,
          color: this.rndElement(this.colors),
          start: this.createStart,
          end: this.createStart + 0.5 * 3600 * 1000,
          timed: true,
          valid: true,
          request: false,
        };

        this.events.push(this.createEvent);
        this.index = this.events.indexOf(this.createEvent);
        this.selfUserEvents.push(this.createEvent);
        this.checkAvailability();
      }
    },
    extendBottom(event) {
      this.createEvent = event;
      this.createStart = event.start;
      this.extendOriginal = event.end;
    },
    mouseMove(tms) {
      const mouse = this.toTime(tms);
      if (
        this.dragEvent &&
        this.dragTime !== null &&
        !this.reservation_created
      ) {
        const start = this.dragEvent.start;
        const end = this.dragEvent.end;
        const duration = end - start;
        const newStartTime = mouse - this.dragTime;
        const newStart = this.roundTime(newStartTime);
        const newEnd = newStart + duration;

        this.dragEvent.start = newStart;
        this.dragEvent.end = newEnd;
        this.checkAvailability();
      } else if (this.createEvent && this.createStart !== null) {
        const mouseRounded = this.roundTime(mouse, false);
        const min = Math.min(mouseRounded, this.createStart);
        let max = Math.max(mouseRounded, this.createStart);

        if (max - min > 2 * 3600 * 1000) {
          max = min + 2 * 3600 * 1000;
        }
        this.createEvent.start = min;
        this.createEvent.end = max;
      }
    },
    endDrag() {
      this.setEvent(this.events[this.index]);
      this.dragTime = null;
      this.dragEvent = null;
      this.createEvent = null;
      this.createStart = null;
      this.extendOriginal = null;
    },
    cancelDrag() {
      if (this.createEvent) {
        if (this.extendOriginal) {
          this.createEvent.end = this.extendOriginal;
        } else {
          const i = this.events.indexOf(this.createEvent);
          if (i !== -1) {
            this.events.splice(i, 1);
          }
        }
      }

      this.createEvent = null;
      this.createStart = null;
      this.dragTime = null;
      this.dragEvent = null;
    },
    roundTime(time, down = true) {
      const roundTo = 30; // minutes
      const roundDownTime = roundTo * 60 * 1000;

      return down
        ? time - (time % roundDownTime)
        : time + (roundDownTime - (time % roundDownTime));
    },
    toTime(tms) {
      return new Date(
        tms.year,
        tms.month - 1,
        tms.day,
        tms.hour,
        tms.minute
      ).getTime();
    },
    getEventColor(event) {
      const rgb = parseInt(event.color.substring(1), 16);
      const r = (rgb >> 16) & 0xff;
      const g = (rgb >> 8) & 0xff;
      const b = (rgb >> 0) & 0xff;

      return event === this.dragEvent
        ? `rgba(${r}, ${g}, ${b}, 0.7)`
        : event === this.createEvent
        ? `rgba(${r}, ${g}, ${b}, 0.7)`
        : event.color;
    },
    getEvents(response) {
      response.forEach((element) => {
        let aux_vec = [];
        //const schedule_date = element.schedule.date_start.split("-");
        const schedule_date = this.dateReservation.split("-");
        const schedule_time_start = element.schedule.start_time.split(":");
        const schedule_time_end = element.schedule.end_time.split(":");

        aux_vec[0] = schedule_date[0];
        aux_vec[1] = schedule_date[1];
        aux_vec[2] = schedule_date[2];
        aux_vec[3] = schedule_time_start[0];
        aux_vec[4] = schedule_time_start[1];
        const date2time_start = this.dateTotime(aux_vec);

        aux_vec[3] = schedule_time_end[0];
        aux_vec[4] = schedule_time_end[1];
        const date2time_end = this.dateTotime(aux_vec);

        this.createEvent = {
          name: `${element.user.name} separó el elemento: ${element.element}`,
          color: this.rndElement(this.colors),
          start: date2time_start,
          end: date2time_end,
          timed: true,
          valid: true,
          request: true,
        };
        this.events.push(this.createEvent);
        this.apiResponse.push(this.createEvent);
      });
    },
    dateTotime(date) {
      return new Date(
        date[0],
        parseInt(date[1], 10) - 1,
        date[2],
        date[3],
        date[4]
      ).getTime();
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
    rndElement(arr) {
      return arr[this.rnd(0, arr.length - 1)];
    },
    setEvent(event) {
      if (this.date.length == 1) {
        this.date.push(this.date[0]);
      }
      this.reserveSubmit = {
        schedule: {
          date: this.date,
          start: new Date(event.start).toString().substr(16, 8),
          end: new Date(event.end).toString().substr(16, 8),
        },
        element: {
          name: this.item.name,
          code: this.item.code,
        },
        user: {
          username: this.selfUser.username,
        },
        quantity: this.quantity,
      };

      if (!event.request) {
        this.checkAvailability();
      }
    },
    checkAvailability() {
      let allowedSchedule = {
        date: this.date[0],
        start1: "08:00",
        end1: "12:00",
        start2: "14:00",
        end2: "21:00",
      };

      let getTime1 = this.dateTotime(
        this.convertDataIntoArray(allowedSchedule.date, allowedSchedule.start1)
      );
      let getTime2 = this.dateTotime(
        this.convertDataIntoArray(allowedSchedule.date, allowedSchedule.end1)
      );
      let getTime3 = this.dateTotime(
        this.convertDataIntoArray(allowedSchedule.date, allowedSchedule.start2)
      );
      let getTime4 = this.dateTotime(
        this.convertDataIntoArray(allowedSchedule.date, allowedSchedule.end2)
      );
      try {
        let auxEvent = this.events[this.index];
        if (
          (auxEvent.start >= getTime1 &&
            auxEvent.start < getTime2 &&
            auxEvent.end <= getTime2) ||
          (auxEvent.start >= getTime3 &&
            auxEvent.start < getTime4 &&
            auxEvent.end <= getTime4)
        ) {
          if (this.index == 0) {
            this.snackbar = false;
            this.events[this.index].valid = true;
            this.disabled = false;
          } else {
            for (var i = 0; i < this.index; i++) {
              if (
                auxEvent.end - auxEvent.start <
                this.events[i].end - this.events[i].start
              ) {
                if (
                  (auxEvent.start >= this.events[i].start &&
                    auxEvent.start < this.events[i].end) ||
                  (auxEvent.end > this.events[i].start &&
                    auxEvent.end < this.events[i].end &&
                    this.index != 0)
                ) {
                  this.snackbar = true;
                  this.events[this.index].valid = false;
                  this.message = "Franja horaria no permitida!";
                  this.disabled = true;
                  break;
                } else {
                  this.snackbar = false;
                  this.events[this.index].valid = true;
                  this.disabled = false;
                }
              } else {
                if (
                  (this.events[i].start >= auxEvent.start &&
                    this.events[i].start < auxEvent.end) ||
                  (this.events[i].end > auxEvent.start &&
                    this.events[i].end < auxEvent.end &&
                    this.index != 0)
                ) {
                  this.snackbar = true;
                  this.events[this.index].valid = false;
                  this.message = "Franja horaria no permitida!";
                  this.disabled = true;
                  break;
                } else {
                  this.snackbar = false;
                  this.events[this.index].valid = true;
                  this.disabled = false;
                }
              }
            }
          }
        } else {
          this.snackbar = true;
          this.events[this.index].valid = false;
          this.message = "Franja horaria no permitida!";
          this.disabled = true;
        }
      } catch (error) {}
    },
    convertDataIntoArray(date, time) {
      let aux_vec = [];
      let dateAsArray = date.split("-");
      let timeAsArray = time.split(":");
      dateAsArray.forEach((element) => {
        aux_vec.push(element);
      });
      timeAsArray.forEach((element) => {
        aux_vec.push(element);
      });
      return aux_vec;
    },
    async getApiInfo() {
      let response = await fetch(
        this.domainBase +
          this.api_dir +
          `?date=${this.dateReservation}&name=${this.item.name}&code=${this.item.code}`,
        {
          method: "GET", // *GET, POST, PUT, DELETE, etc.
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
          },
        }
      );
      response = await response.json();
      return response;
    },
    removeEvent() {
      if (this.events.length > this.apiResponse.length) {
        this.events.pop();
        this.disabled = true;
        this.dragTime = null;
        this.dragEvent = null;
        this.createEvent = null;
        this.createStart = null;
        this.extendOriginal = null;
        this.selfUserEvents = [];
        this.index = null;
      }
    },
    submitReserve() {
      if (!this.reservation_created) {
        this.loading = true;
        let formData = JSON.stringify(this.reserveSubmit);
        fetch(this.domainBase + this.api_post, {
          method: "POST",
          headers: {
            "Content-type": "application/json",
          },
          body: JSON.stringify(formData),
        })
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            this.reservation_created = response.created;
            if (this.reservation_created) {
              this.message = "Reserva guardada exitosamente";
            } else {
              this.message =
                "Un error inesperado ha ocurrido. Intenta de nuevo más tarde.";
            }
            this.loading = false;
            this.snackbar = true;
          })
          .catch(() => {
            this.message =
              "Un error inesperado ha ocurrido. Intenta de nuevo más tarde.";
            this.loading = false;
            this.snackbar = true;
          });
      } else {
        this.snackbar = true;
        this.message =
          "Ya realizaste la reserva. Revisa tu correo para más información.";
      }
    },
  },
};
</script>



<style scoped >
div {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.v-event-draggable {
  padding-left: 6px;
}

.v-event-timed {
  user-select: none;
  -webkit-user-select: none;
}

.v-event-drag-bottom {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 4px;
  height: 4px;
  cursor: ns-resize;
}
.v-event-drag-bottom::after {
  display: none;
  position: absolute;
  left: 50%;
  height: 4px;
  border-top: 1px solid white;
  border-bottom: 1px solid white;
  width: 16px;
  margin-left: -8px;
  opacity: 0.8;
  content: "";
}
.v-event-drag-bottom:hover::after {
  display: block;
}
.submit-reserve {
  position: absolute;
  bottom: 10px;
  right: 20px;
}
.close {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>