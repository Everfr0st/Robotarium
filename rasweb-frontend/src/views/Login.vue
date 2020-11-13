<template>
  <div>
    <v-container>
      <form @submit.prevent="loginSubmit">
        <v-text-field
          v-model="username"
          label="Username"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="password"
          required
        ></v-text-field>

        <v-btn class="mr-4" type="submit"> submit </v-btn>
      </form>
    </v-container>
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
    incorrectAuth: false,
  }),
  computed: {
    ...mapState(["authentication"]),
  },
  mounted(){
      if (this.authentication.auth){
          this.$router.push({ name: "Home" });
      }
  },
  methods: {
    ...mapMutations(["updateAuthcredentials"]),
    async loginSubmit() {
        let form_data = {
          username: this.username,
          password: this.password
        }
   
        var response = await fetch(web_domain + 'api-token/', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'content-type': 'application/json'
          },
          body: JSON.stringify(form_data)
        })
        if (response.status === 200){
        response = await response.json()
        this.updateAuthcredentials({
          access: response.access,
          refresh: response.refresh,
          auth: true,
        })
        this.$router.push({name: 'Home'})
      }   
    },
  },
};
</script>