<template>
  <div>
    <v-app-bar app class="NavBar" dark>
      <div class="d-flex align-center">
        <v-btn :to="{ name: 'Home' }" id="logo-btn">
          <h1>LOGO</h1>
        </v-btn>
      </div>
      <v-spacer></v-spacer>

      <v-btn fab text>
        <v-icon>mdi-comment-text</v-icon>
      </v-btn>
      <v-btn fab text>
        <v-icon>mdi-bell</v-icon>
      </v-btn>
      <v-btn fab text>
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>

const web_domain = "http://127.0.0.1:8000";
export default {
  name: "NavBar",
  data: () => ({}),
  async created() {
    const api_dir = "/coco-api/v1.0/navbar-info";
      let nav_data = await fetch(web_domain + api_dir).then((response) => {
        console.log(nav_data);
      });
  },
  mounted() {
    const logo = document.getElementById("logo-btn");
    logo.classList.remove("v-btn--active", "v-btn--contained");

  },
  methods: {
    
  },
};
</script>

<style>
.NavBar {
  background: rgba(89, 4, 4, 1);
  background: -moz-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -webkit-gradient(
    left top,
    right top,
    color-stop(0%, rgba(89, 4, 4, 1)),
    color-stop(30%, rgba(192, 7, 7, 1)),
    color-stop(100%, rgba(192, 7, 7, 1))
  );
  background: -webkit-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -o-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -ms-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  background: linear-gradient(
    to right,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 30%,
    rgba(192, 7, 7, 1) 100%
  );
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#590404', endColorstr='#c00707', GradientType=1 );
}
#logo-btn {
  color: white;
  background: transparent;
  border: 0px;
}
</style>