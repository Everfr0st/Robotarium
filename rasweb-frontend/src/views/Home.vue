<template>
  <div>
    <v-card elevation="0">
      <v-container fluid>
        <v-progress-linear
          v-if="loading"
          class="mb-2"
          :active="loading"
          :indeterminate="loading"
          color="accent"
        ></v-progress-linear>
        <form action="">
          <v-row class="pl-3" justify="start" align="center">
            <v-avatar>
              <v-avatar size="50" color="blue" v-if="self_user.profile_picture">
                <img :src="self_user.profile_picture" :alt="self_user.name" />
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

          <v-row v-if="tagUsers" class="pt-0" justify="center">
            <v-form style="width: 96%">
              <v-container>
                <v-row>
                  <v-autocomplete
                    v-model="tagUserslist"
                    :items="users"
                    chips
                    color="accent lighten-2"
                    label="¿Con quién vas a anunciar?"
                    item-text="name"
                    item-value="username"
                    multiple
                  >
                  
                    <template v-slot:selection="data">
                      <v-chip
                        v-bind="data.attrs"
                        :input-value="data.selected"
                                              >
                        <v-avatar left v-if="data.item.profile_picture">
                          <img
                            :src="data.item.profile_picture"
                            :alt="data.item.name"
                          />
                        </v-avatar>
                        <v-avatar left color="secondary" v-else>
                          <span
                            v-if="data.item.name"
                            style="color: white; font-size: 8pt"
                            >{{ data.item.name.split(" ")[0].slice(0, 1)
                            }}{{
                              data.item.name.split(" ")[1].slice(0, 1)
                            }}</span
                          >
                          <span v-else style="color: white; font-size: 8pt">{{
                            data.item.username.slice(0, 2).toUpperCase()
                          }}</span>
                        </v-avatar>
                        {{
                          data.item.name
                            ? data.item.name
                            : "@" + data.item.username
                        }}
                      </v-chip>
                    </template>
                    <template v-slot:item="data">
                      <template v-if="typeof data.item !== 'object'">
                        <v-list-item-content
                          v-text="data.item"
                        ></v-list-item-content>
                      </template>
                      <template v-else>
                        <v-list-item-avatar
                          left
                          v-if="data.item.profile_picture"
                        >
                          <img
                            :src="data.item.profile_picture"
                            :alt="data.item.name"
                          />
                        </v-list-item-avatar>
                        <v-list-item-avatar left color="secondary" v-else>
                          <span
                            v-if="data.item.name"
                            style="color: white; font-size: 8pt"
                            >{{ data.item.name.split(" ")[0].slice(0, 1)
                            }}{{
                              data.item.name.split(" ")[1].slice(0, 1)
                            }}</span
                          >
                          <span v-else style="color: white; font-size: 8pt">{{
                            data.item.username.slice(0, 2).toUpperCase()
                          }}</span>
                        </v-list-item-avatar>

                        <v-list-item-content>
                          <v-list-item-title
                            v-html="data.item.name"
                          ></v-list-item-title>
                          <v-list-item-subtitle
                            v-html="'@' + data.item.username"
                          ></v-list-item-subtitle>
                        </v-list-item-content>
                      </template>
                    </template>
                  </v-autocomplete>
                </v-row>
              </v-container>
            </v-form>
          </v-row>
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
                  <span v-if="photos.length"> ({{ photos.length }})</span>
                </v-btn>
              </template>
              <v-card>
                <v-container class="ma-0 pa-0" style="overflow: hidden">
                  <v-row>
                    <v-carousel v-if="photos.length">
                      <v-carousel-item
                        v-for="(photo, i) in photos"
                        :key="i"
                        :src="photo.src"
                      >
                        <v-chip
                          style="
                            position: absolute;
                            right: 15px;
                            top: 5px;
                            cursor: pointer;
                          "
                          close
                          @click="
                            photos.splice(i, 1);
                            files.splice(i, 1);
                          "
                          >Eliminar</v-chip
                        >
                      </v-carousel-item>
                    </v-carousel>
                    <v-card-text v-else align="center">
                      <h1>Selecciona las fotos</h1>
                      <v-file-input
                        class="ma-3"
                        chips
                        counter
                        multiple
                        show-size
                        truncate-length="1"
                        @change="setImagearray"
                        accept="image/*"
                        prepend-icon="mdi-camera"
                      ></v-file-input>
                    </v-card-text>
                  </v-row>
                </v-container>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    v-if="photos.length"
                    color="primary"
                    @click="
                      photos = [];
                      files = [];
                    "
                    >Eliminar todas</v-btn
                  >
                  <v-btn color="accent" outlined @click="dialog = false">
                    Listo!
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-btn text class="ml-2" @click="tagUsers = !tagUsers">
              <template>
                <img
                  class="mr-1"
                  width="24"
                  height="24"
                  src="@/assets/icons/tag_friend.svg"
                />
              </template>
              Etiquetar usuarios
              <span v-if="tagUserslist.length"
                >({{ tagUserslist.length }})</span
              >
            </v-btn>
            <v-btn
              :disabled="loading"
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
    
      <PubList />
    
    <v-snackbar v-model="snackbar" :timeout="timeout">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="error"
          outlined
          v-bind="attrs"
          @click="snackbar = false"
        >
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from "vuex";
import PubList from "@/components/PubList.vue";

export default {
  name: "Home",
  components: {
    PubList,
  },
  data: () => ({
    content: "",
    photos: [],
    files: [],
    tagUserslist: [],
    dialog: false,
    loading: false,
    tagUsers: false,
    snackbar: false,
    timeout: 5000,
    message: "",
    attrs: ''
  }),
  computed: {
    ...mapState(["users", "self_user", "authentication"]),
  },
  methods: {
    AddContent() {
      var divContent = document.getElementById("create-post");
      this.content = divContent.innerText;
    },
    async submitPost() {
      if (this.content.length || this.files.length) {
        this.loading = true;
        const web_domain = "http://127.0.0.1:8000";
        const api_dir = "/coco-api/v1.0/new-post/";

        const formdata = new FormData();
        formdata.append("username", this.self_user.username);
        formdata.append("content", this.content);
        formdata.append("num_photos", this.photos.length);
        formdata.append("num_users", this.tagUserslist.length);
        this.files.forEach((file) => {
          formdata.append(`photo_${this.files.indexOf(file)}`, file);
        });
        console.log(this.tagUserslist);
        this.tagUserslist.forEach((user) => {
          formdata.append(`user_${this.tagUserslist.indexOf(user)}`, user);
        });

        const options = {
          method: "POST",
          headers: {},
          body: formdata,
        };
        delete options.headers["Content-Type"];

        let response = await fetch(web_domain + api_dir, options);
        response = await response.json();
        if (!response.created) {
          this.message =
            "Ha sucedido un error inesperado, intenta de nuevo más tarde.";
          this.snackbar = true;
        } else {
          this.loading = false;
          this.content = "";
          this.photos = [];
          this.files = [];
          this.tagUserslist = [];
          this.tagUsers = false;
          var divContent = document.getElementById("create-post");
          divContent.innerText = "";
        }
      } else {
        this.message = "Debes agregar contenido a tu publicación!";
        this.snackbar = true;
      }
    },
    setImagearray(photos) {
      photos.forEach((photo) => {
        this.photos.push({ src: URL.createObjectURL(photo) });
        this.files.push(photo);
      });
    },
    remove(item) {
      const index = this.users.indexOf(item);
      if (index >= 0) this.users.splice(index, 1);
    },
  },
  
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
