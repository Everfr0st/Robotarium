<template>
  <div>
    <v-container class="px-0" fluid>
      <v-card elevation="3">
        <v-form @submit.prevent="getHistory(); recent=false;">
          <v-row class="px-5" justify="center">
            <v-col cols="12" sm="6" md="4">
              <v-text-field v-model="query" label="Elemento"></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col cols="12" sm="6" md="3">
              <v-menu
                v-model="menu1"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="dateStart"
                    label="Desde"
                    prepend-icon="mdi-calendar-cursor"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="dateStart"
                  @input="menu2 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-menu
                v-model="menu2"
                :close-on-content-click="false"
                :nudge-right="40"
                transition="scale-transition"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="dateEnd"
                    label="Hasta"
                    prepend-icon="mdi-calendar-cursor"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="dateEnd"
                  @input="menu2 = false"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col md="2">
              <v-card-actions>
                <v-btn :loading="loading" class="mx-auto" type="submit" color="accent darken-3"
                  >Buscar</v-btn
                >
              </v-card-actions>
            </v-col>
            <v-spacer></v-spacer>
          </v-row>
        </v-form>
         <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        bottom
        color="accent accent-4"
      ></v-progress-linear>
      </v-card>
    </v-container>

    <div v-if="recent" class="display-1 mt-3 px-3">Reservas agendadas para hoy</div>
    <div class="mt-5 px-3">{{ msg }}</div>
    <v-card
      elevation="5"
      v-for="(reservation, index) in historyList"
      :key="index"
      class="mt-5 mb-10"
    >
      <ReservationInHistory :reservation="reservation" />
    </v-card>
    <v-snackbar v-model="snackbar">
      {{ message }}

      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";
import ReservationInHistory from "@/components/subcomponents/ReservationInHistory.vue";
export default {
  name: "History",
  components: {
    ReservationInHistory,
  },
  data: () => ({
    apiDir: "/robotarium-api/v1.0/history-reservation/",
    query: "",
    dateStart: new Date().toISOString().substr(0, 10),
    dateEnd: new Date().toISOString().substr(0, 10),
    historyList: [],
    menu1: false,
    menu2: false,
    snackbar: false,
    message: "",
    msg: "",
    loading: false,
    recent: true
  }),
  computed: {
    ...mapState(["domainBase", "authentication"]),
  },
  created() {
    this.getHistory();
  },
  methods: {
    getHistory() {
      this.loading = true;
      if (this.dateStart <= this.dateEnd) {
        fetch(
          this.domainBase +
            this.apiDir +
            `?query=${this.query}&dateStart=${this.dateStart}&dateEnd=${this.dateEnd}`,
          {
            headers: {
              Authorization: `Token ${this.authentication.accessToken}`,
            },
          }
        )
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            this.historyList = response;
            if (this.historyList.length) {
              this.msg = `Encontramos ${
                response.length == 1
                  ? "una reserva 😎"
                  : response.length + " reservas 😎"
              }`;
            } else {
              if(this.recent) this.msg = "No hay reservas agendadas para el día de hoy 🤨" 
              else this.msg = "No encontramos reservas con la información que suministraste 🤔";
            }
          })
          .catch(function (error) {
            console.log(error);
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.snackbar = true;
        this.message = "Debes introducir un rango de fechas válido!";
      }
    },
  },
};
</script>

<style>
</style>