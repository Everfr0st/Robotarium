<template>
  <div>
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>Actualiza tu foto de perfil</v-card-title>
        <v-card-text class="text-center">
          <v-avatar size="150" class="ma-5" color="secondary">
            <v-img v-if="url" class="mx-auto" :src="url"> </v-img>
            <span class="white--text" v-else>
              {{ selfUser.name.slice(0, 1) }}
            </span>
          </v-avatar>
          <v-file-input
            accept="image/png, image/jpeg, image/bmp"
            placeholder="Tu foto de perfil"
            prepend-icon="mdi-camera"
            label="Foto de perfil"
            v-model="photo"
          ></v-file-input>
          <v-btn @click="uploadProfilePicture" :loading="loading" :disabled="!photo" class="mt-3" block color="accent darken-3"
            >Subir</v-btn
          >
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "ProfilePicture",
  data: () => ({
    photo: "",
    dialog: true,
    loading: false,
    apiDir: "/robotarium-api/v1.0/user-profile-picture/"
  }),
  computed: {
    ...mapState(["selfUser", "authentication", "domainBase"]),
    url: function () {
      if (this.photo) {
        return URL.createObjectURL(this.photo);
      } else if (this.selfUser.profile_picture) {
        return this.selfUser.profile_picture;
      }
      return "";
    },
  },
  watch:{
    dialog(){
      if(!this.dialog){
        this.$emit("closed")
      }
    }
  },
  methods:{
      uploadProfilePicture() {
      this.loading = true;
      if (this.photo) {
        const formData = new FormData();
        formData.append("profile_picture", this.photo);
        let headers = {
          Authorization: `Token ${this.authentication.accessToken}`,
        };
        delete headers["Content-Type"];
        fetch(this.domainBase + this.apiDir, {
          method: "PUT",
          headers: headers,
          body: formData,
        })
          .then((response) => response.json())
          .then((response) => {
              this.dialog = false;
              location.href ="/";
          })
          .catch((err) => console.error(err))
          .finally(() => {
            
            this.loading = false;
          });
      }
    },
  }
};
</script>

<style>
</style>