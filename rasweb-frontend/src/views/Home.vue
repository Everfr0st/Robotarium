<template>
  <div>
    <v-card elevation="0">
      <v-container fluid>
        <form action="">
          <v-row class="pl-3" justify="start" align="center" wrap>
            <v-avatar>
              <v-avatar size="50" color="blue" v-if="self_user.profile_picture">
                <img :src="self_user.profile_picture" :alt="name" />
              </v-avatar>
              <v-avatar size="50" color="secondary" v-else>
                <span v-if="self_user.name" style="color: white"
                  >{{ self_user.name.split(" ")[0].slice(0, 1)
                  }}{{ self_user.name.split(" ")[1].slice(0, 1) }}</span
                >
                <span v-else style="color: white">{{
                  self_user.username.slice(0, 2).toUpperCase()
                }}</span>
              </v-avatar>
            </v-avatar>
            <span class="ml-2" style="width: 90%">
              <div
                data-placeholder="Edit me"
                contenteditable="true"
                class="create"
                id="create-post"
                placeholder="¿Deseas anunciar algo?"
                @keyup="AddContent()"
              ></div>
            </span>
          </v-row>
          <v-divider class="mt-2 mb-2"></v-divider>
          <v-row class="pl-2">
            <v-dialog v-model="dialog" persistent max-width="600">
              <template v-slot:activator="{ on, attrs }">
                <v-btn text v-bind="attrs" v-on="on">
                  <template>
                    <img
                      class="mr-1"
                      width="24"
                      height="24"
                      src="@/assets/icons/upload_photo.svg"
                    />
                  </template>
                  Subir fotos
                </v-btn>
              </template>
              <v-card>
                <v-container class="ma-0 pa-0" style="overflow: hidden">
                  <v-row>
                    <v-carousel v-if="photos.length">
                      <v-carousel-item
                        v-for="(item, i) in photos"
                        :key="i"
                        :src="item.src"
                      ></v-carousel-item>
                    </v-carousel>
                    
                  </v-row>
                </v-container>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="green darken-1" text @click="dialog = false">
                    Disagree
                  </v-btn>
                  <v-btn color="green darken-1" text @click="dialog = false">
                    Agree
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-btn text class="ml-2">
              <template>
                <img
                  class="mr-1"
                  width="24"
                  height="24"
                  src="@/assets/icons/tag_friend.svg"
                />
              </template>
              Etiquetar usuarios
            </v-btn>
            <v-btn
              @click="submitPost()"
              color="primary"
              rounded
              class="ml-auto mr-3"
              >Publicar</v-btn
            >
          </v-row>
        </form>
        <v-divider class="mt-2 mb-2"></v-divider>
      </v-container>
    </v-card>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from "vuex";

export default {
  name: "Home",

  data: () => ({
    content: "",
    photos: [
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/sky.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/bird.jpg",
      },
      {
        src: "https://cdn.vuetifyjs.com/images/carousel/planet.jpg",
      },
    ],
    dialog: false,
  }),
  computed: {
    ...mapState(["self_user", "authentication"]),
  },
  methods: {
    AddContent() {
      var divContent = document.getElementById("create-post");
      this.content = divContent.innerText;
    },
    async submitPost() {
      const web_domain = "http://127.0.0.1:8000";
      const api_dir = "/coco-api/v1.0/new-post/";
      let formData = {
        content: this.content,
      };
      let response = await fetch(web_domain + api_dir, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          Authorization: `Bearer ${this.authentication.accessToken}`,
        },
        body: JSON.stringify(formData),
      });
    },
  },
  components: {},
};
</script>

<style scoped>
.create {
  width: auto;
  min-height: 16pt;
  height: auto;
  max-height: 100px;
  overflow: auto;
  overflow-x: hidden;
}
.create:hover {
  cursor: text;
}
.create:focus {
  outline: none;
  cursor: text;
}

[contenteditable][placeholder]:empty:before {
  content: attr(placeholder);
  position: absolute;
  color: gray;
  background-color: transparent;
}
</style>
