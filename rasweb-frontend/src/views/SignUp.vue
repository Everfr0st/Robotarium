<template>
  <div>
    <v-img class="bg" src="@/assets/images/bg.jpg">
      <v-container class="container">
        <v-row class="row-form">
          <v-col class="login-form" sm="12" md="6">
            <v-row>
              <v-img
                max-height="70"
                max-width="70"
                src="@/assets/logo/LogoSir.svg"
              ></v-img>
              <h1 class="mt-3">RAS-UAO</h1>
            </v-row>

            <v-btn elevation="2" block class="google-button" dark large>
              <v-img
                class="google-logo"
                src="https://img.icons8.com/color/452/google-logo.png"
              ></v-img>
              Regístrate con Google
            </v-btn>

            <v-row class="pa-3 mr-1">
              <v-col class="pa-2" sm="5"><div class="line"></div></v-col>
              <v-col class="pa-2" sm="2"
                ><h3 style="text-align: center">Ó</h3></v-col
              >
              <v-col class="pa-2" sm="5"><div class="line"></div></v-col>
            </v-row>

            <form @submit.prevent="loginSubmit">
              <v-text-field
                class="mb-1"
                v-model="username"
                label="Usuario"
                :rules="[rules.required]"
              ></v-text-field>
              <v-text-field
                class="mb-1"
                v-model="password"
                label="Contraseña"
                :type="view ? 'text' : 'password'"
                :rules="[rules.required]"
                :append-icon="view ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="view = !view;"
              ></v-text-field>
              
              <v-progress-linear
                v-if="loading"
                color="accent"
                indeterminate
                rounded
                height="6"
              ></v-progress-linear>
              <v-btn class="mr-4" color="primary" block type="submit">
                Regístrate
              </v-btn>
            </form>
            <v-row class="mt-2" justify="center">
                <p style="margin-top: 2px;" >¿No tienes una cuenta?</p>
                <v-btn class="ml-1"  small text color="primary">Regístrate</v-btn>
            </v-row>
          </v-col>
          <v-col class="image-login">
            <v-img src="@/assets/images/circuit.png" class="circuit"></v-img>

            <v-img src="@/assets/images/Duckie_logo.png" class="duckie"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-img>
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
import { mapState, mapMutations } from "vuex";
const web_domain = "http://127.0.0.1:8000/robotarium-api/v1.0/";

export default {
  name: "Login",
  data: () => ({
    username: "",
    password: "",
    loading: false,
    incorrectAuth: false,
    snackbar: false,
    message: "",
    view: false,
    rules: {
      required: (value) => !!value || "Obligatorio",
    },
  }),
  computed: {
    ...mapState(["authentication"]),
  },
  mounted() {
    if (this.authentication.auth) {
      this.$router.push({ name: "Home" });
    }
  },
  created() {
    document.title = "SignUp · UAO-RAS";
    this.setViewname("SignUp");
  },
  methods: {
    ...mapMutations(["updateAuthcredentials", "setViewname"]),
    async loginSubmit() {
      this.loading = true;
      let form_data = {
        username: this.username,
        password: this.password,
      };

      var response = await fetch(web_domain + "api-token/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(form_data),
      });
      if (response.status === 200) {
        response = await response.json();
        this.updateAuthcredentials({
          access: response.access,
          refresh: response.refresh,
          auth: true,
        });
        this.$router.push({ name: "Home" });
      } else {
        this.snackbar = true;
        this.message = "Credenciales inválidas!";
      }
      this.loading = false;
    },
  },
};
</script>

<style scoped>
h1 {
  color: #424242;
}
.bg {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100vw;
  height: 100vh;
}
.overlay {
  position: fixed;
  top: 0px;
  left: 0px;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1;
}
.container {
  width: 100vw;
  height: 40px;
  margin: 5% auto;
}
.row-form {
  padding: 2%;
  border-radius: 15px;
}
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
.line {
  background: rgba(192, 7, 7, 1) 100%;
  margin: 12px 5px;
  width: 100%;
  height: 3px;
  border-radius: 2px;
}
.forgot-password {
  font-size: 10pt;
  -webkit-user-select: none;
  -moz-user-select: none;
  -khtml-user-select: none;
  -ms-user-select: none;
}
.forgot-password:hover {
  text-decoration: underline;
  cursor: pointer;
}
.image-login {
  background: #be0707;
  border-radius: 0 10px 10px 0;
  position: relative;
}
.login-form {
  background: white;
  border-radius: 10px 0 0 10px;
}
.circuit {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  opacity: 0.4;
}
.duckie {
  display: block;
  width: 400px;
  height: auto;
  margin: 12% auto;
}
@media (max-width: 960px) {
  .image-login {
    display: none;
  }
  .login-form {
    width: 100%;
  }
  .row-form {
    margin: 5px;
  }
}
</style>