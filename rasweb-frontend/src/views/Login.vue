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

            <social-login> 
              Inicia sesión
            </social-login>

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
                label="Usuario o correo"
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
              <p class="forgot-password">¿Olvidaste tu contraseña?</p>
              <v-progress-linear
                v-if="loading"
                color="accent"
                indeterminate
                rounded
                height="6"
              ></v-progress-linear>
              <v-btn class="mr-4" color="primary" block type="submit">
                Iniciar sesión
              </v-btn>
            </form>
            <p class="mt-3 mb-0" align="center" >
            ¿No tienes una cuenta? <a @click="go2SignUpView">Regístrate</a>
          </p>
          </v-col>
          <v-col class="image-login">
            <v-img src="@/assets/images/circuit.png" class="circuit"></v-img>

            <v-img src="@/assets/images/Duckie_logo.png" class="duckie pa-0"></v-img>
          </v-col>
        </v-row>
      </v-container>
    </v-img>
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
import SocialLogin from '../components/SocialLogin.vue';

export default {
  components: { SocialLogin },
  name: "Login",
  data: () => ({
    username: "",
    password: "",
    loading: false,
    incorrectAuth: false,
    snackbar: false,
    message: "",
    apiDir: "/robotarium-api/v1.0/user-auth/login/",
    view: false,
    rules: {
      required: (value) => !!value || "Obligatorio",
    },
  }),
  computed: {
    ...mapState(["authentication", "domainBase"]),
  },
  mounted() {
    if (this.authentication.auth) {
      this.$router.push({ name: "Home" });
    }
  },
  created() {
    document.title = "Login · UAO-RAS";
    this.setViewname("Login");
  },
  methods: {
    ...mapMutations(["updateAuthcredentials", "setViewname"]),
    loginSubmit() {
      
      this.loading = true;
      if(this.username){
        let form_data = {};
      if (this.username.indexOf("@") > -1) {
        form_data = {
          username: "",
          email: this.username,
          password: this.password,
        };
      } else {
        form_data = {
          username: this.username,
          email: "",
          password: this.password,
        };
      }
     
      fetch(this.domainBase + this.apiDir, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(form_data),
      })
      .then((response)=>{       
          if(response.status == 200){

            return response.json()
          }
      })
      .then((response)=>{
          this.updateAuthcredentials({
          access: response.key,
          auth: true,
        });
        this.$router.push({ name: "Home" });
      })
      .catch((err)=>{
        this.snackbar = true;
        this.message = "Credenciales inválidas!";
      })
      .finally(()=>{
        this.loading = false;
      })

      } else{
        this.snackbar = true;
        this.message = "Debes ingresar datos!"
        this.loading = false;
      }      
    },
    go2SignUpView(){
      this.$router.push({name:"SignUp"})
    }
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
  height: auto;
  margin: 5% auto;
}
.row-form {
  border-radius: 15px;
  max-height: 480px;
  overflow: hidden;
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
  padding: 25px;
}
.circuit {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  border-radius: inherit;
}
.duckie {
  display: block;
  width: 400px;
  height: auto;
  margin: 20% auto;
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
p,
a {
  font-size: 12pt;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>