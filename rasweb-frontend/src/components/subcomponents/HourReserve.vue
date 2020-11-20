<template>
  <div>
    <v-card>
      <v-card-title>
        Franja horaria permitida: 8am - 12m y 2pm - 6pm
      </v-card-title>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="date"
          first-time="08:00"
          :event-more="true"
          color="primary"
          type="day"
          event-overlap-mode="stack"
          :events="events"
          :event-color="getEventColor"
          :event-ripple="false"
          @mousedown:event="startDrag"
          @mousedown:time="startTime"
          @mousemove:time="mouseMove"
          @mouseup:time="endDrag"
          @mouseleave.native="cancelDrag"
          @mouseup:event="setEvent"
        >
          <template   v-slot:event="{ event, timed, eventSummary }">
            <v-row :title="!valid? 'Ajusta tu franja horaria':''" class="pa-0 ml-1 pt-2">
              <v-icon v-if="!valid" class="ml-3" color="error">mdi-alert</v-icon
              >
              <div class="v-event-draggable" v-html="eventSummary()"></div>
            </v-row>

            <div
              v-if="timed"
              class="v-event-drag-bottom"
              @mousedown.stop="extendBottom(event)"
            ></div>
          </template>
        </v-calendar>
      </v-sheet>
    </v-card>
    <v-snackbar v-model="snackbar" timeout="5000">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" outlined v-bind="attrs" @click="snackbar = false">
          Cerrar
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
    colors: [
      "#2196F3",
      "#3F51B5",
      "#673AB7",
      "#00BCD4",
      "#4CAF50",
      "#FF9800",
      "#757575",
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
  }),
  computed: {
    ...mapState(["self_user"]),
  },
  methods: {
    startDrag({ event, timed }) {
      if (event && timed) {
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
      } else if (this.events.length < 1) {
        this.createStart = this.roundTime(mouse);
        this.createEvent = {
          name: `${this.self_user.name} separa el elemento: ${this.item.name}`,
          color: this.rndElement(this.colors),
          start: this.createStart,
          end: this.createStart + 0.5 * 3600 * 1000,
          timed: true,
        };

        this.events.push(this.createEvent);
      }
    },
    extendBottom(event) {
      this.createEvent = event;
      this.createStart = event.start;
      this.extendOriginal = event.end;
    },
    mouseMove(tms) {
      const mouse = this.toTime(tms);

      if (this.dragEvent && this.dragTime !== null) {
        const start = this.dragEvent.start;
        const end = this.dragEvent.end;
        const duration = end - start;
        const newStartTime = mouse - this.dragTime;
        const newStart = this.roundTime(newStartTime);
        const newEnd = newStart + duration;

        this.dragEvent.start = newStart;
        this.dragEvent.end = newEnd;
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

    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a;
    },
    rndElement(arr) {
      return arr[this.rnd(0, arr.length - 1)];
    },
    setEvent(event) {
      let tempObj = {
        date: this.date,
        start_time: event.eventParsed.start.time,
        end_time: event.eventParsed.end.time,
      };
      console.log(tempObj);
      let aux_start_hours = parseInt(tempObj.start_time.split(":")[0], 10);
      let aux_start_min = parseInt(tempObj.start_time.split(":")[1], 10);
      let aux_end_hours = parseInt(tempObj.end_time.split(":")[0], 10);
      let aux_end_min = parseInt(tempObj.end_time.split(":")[1], 10);

      let start = 0;
      let end = 0;
      if (
        aux_start_hours < 8 ||
        (aux_start_hours >= 12 && aux_start_hours < 14) ||
        aux_start_hours >= 18 ||
        ((aux_end_hours > 12 || (aux_end_hours == 12 && aux_end_min == 30)) &&
          aux_end_hours <= 14) ||
        aux_end_hours > 18 ||
        (aux_end_hours == 18 && aux_end_min == 30)
      ) {
        this.snackbar = true;
        this.valid = false;
        this.message = "Franja horaria no permitida!";
      } else {
        this.snackbar = false;
        this.valid = true;
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
</style>