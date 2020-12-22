<template>
  <div>
    <v-list two-line v-if="userInfo" >
      <v-list-item>
        <v-list-item-avatar  color="secondary">
          <v-img
            v-if="userInfo.profile_picture"
            :alt="userInfo.name"
            :src="userInfo.profile_picture"
          ></v-img>
          <span v-else class="white--text">{{
            userInfo.name.slice(0, 1)
          }}</span>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
              {{userInfo.name}} 
              
          </v-list-item-title>

          <v-list-item-subtitle>
            @{{ userInfo.username }} ·
            <span :title="'🕒 '+timeSince">
              <v-icon  small> mdi-history </v-icon>
              {{timeSince}}
            </span>
            
          </v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn large title="Reportar" icon color="primary">
            <v-icon>mdi-alert-octagon</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
      <v-card-title v-if="elementInfo" class="pt-0 mt-0"
        >Reservó el elemento {{ elementInfo.name }} que se encuentra en la
        posición {{ elementInfo.code }}</v-card-title
      >
      <v-card-subtitle v-if="scheduleInfo">
        <v-icon left>mdi-calendar-clock</v-icon>
        {{ scheduleInfo.date }}, de {{ scheduleInfo.start_time.substr(0, 5) }} a
        {{ scheduleInfo.end_time.substr(0, 5) }}
      </v-card-subtitle>
      <v-img :src="elementInfo.photo"></v-img>
    </v-list>
  </div>
</template>

<script>
import { mapState } from "vuex";
import moment from 'moment';
export default {
  name: "ReservationInHistory",
  props: ["reservation"],
  data: () => ({
    userInfo: "",
    scheduleInfo: "",
    elementInfo: "",
    apiDir: {
      userInfo: "/robotarium-api/v1.0/user-Info/",
      scheduleInfo: "/robotarium-api/v1.0/schedule-Info/",
      elementInfo: "/robotarium-api/v1.0/element-Info/",
    },
  }),
  computed: {
    ...mapState(["authentication", "domainBase"]),

    timeSince: function(){
        return moment(this.reservation.created).locale('es').fromNow();
    }
  },
  created() {
                  console.log(moment())
    this.apiRetrieve(
      this.domainBase + this.apiDir.userInfo + `?user=${this.reservation.user}`,
      "userInfo"
    );
    this.apiRetrieve(
      this.domainBase + this.apiDir.elementInfo + `${this.reservation.element}`,
      "elementInfo"
    );
    this.apiRetrieve(
      this.domainBase +
        this.apiDir.scheduleInfo +
        `${this.reservation.schedule}`,
      "scheduleInfo"
    );
  },
  methods: {
    apiRetrieve(url, field) {
      fetch(url, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          if (field == "userInfo") {
            this.userInfo = response;
          } else if (field == "elementInfo") {
            this.elementInfo = response;
          } else {
            this.scheduleInfo = response;
          }
        });
    },
  },
};
</script>

<style>
</style>