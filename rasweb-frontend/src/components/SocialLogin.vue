<template>
  <div>
    <v-btn
      @click="googleSignIn"
      elevation="2"
      block
      class="google-button"
      dark
      large
    >
      <v-img
        width="30"
        height="30"
        class="google-logo"
        src="https://img.icons8.com/color/452/google-logo.png"
      ></v-img>
      <slot></slot>
    </v-btn>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "SocialLogin",
  data() {
    return {
      apiDir: "/robotarium-api/v1.0/user-auth/google/",
      snackbar: false,
      message: "",
      loading: false,
    };
  },
  computed: {
    ...mapState(["domainBase"]),
  },
  methods: {
    ...mapMutations(["updateAuthcredentials"]),
    googleSignIn() {
      this.loading = true;
      this.$gAuth
        .signIn()
        .then((user) => {
          // On success do something, refer to https://developers.google.com/api-client-library/javascript/reference/referencedocs#googleusergetid
          this.backendLogin(user.uc.access_token);
        })
        .catch((error) => {});
    },
    backendLogin(accessToken) {
      console.log(accessToken);
      let formData = {
        access_token: accessToken,
        code: "",
      };
      fetch(this.domainBase + this.apiDir, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.updateAuthcredentials({
            access: response.key,
            auth: true,
          });
          this.$router.push({ name: "Home" });
        })
        .catch((err) => {
          this.snackbar = true;
          this.message = "Ha sucedido un error inesperado.";
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
.google-logo {
  background: white;
  border-radius: 5px;
  width: 35px;
  height: 35px;
  position: absolute;
  left: -15px;
}
.google-button {
  position: relative;
  background: rgba(89, 4, 4, 1);
  background: -moz-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 55%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -webkit-gradient(
    left top,
    right top,
    color-stop(0%, rgba(89, 4, 4, 1)),
    color-stop(55%, rgba(192, 7, 7, 1)),
    color-stop(100%, rgba(192, 7, 7, 1))
  );
  background: -webkit-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 55%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -o-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 55%,
    rgba(192, 7, 7, 1) 100%
  );
  background: -ms-linear-gradient(
    left,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 55%,
    rgba(192, 7, 7, 1) 100%
  );
  background: linear-gradient(
    to right,
    rgba(89, 4, 4, 1) 0%,
    rgba(192, 7, 7, 1) 55%,
    rgba(192, 7, 7, 1) 100%
  );
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#590404', endColorstr='#c00707', GradientType=1 );
}
</style>