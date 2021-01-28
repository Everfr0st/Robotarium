<template>
  <div>
    <v-card elevation="3" class="mb-4" style="border-radius: 15px">
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
              <v-avatar size="50" color="blue" v-if="selfUser.profile_picture">
                <img :src="selfUser.profile_picture" :alt="selfUser.name" />
              </v-avatar>
              <v-avatar size="50" color="secondary" v-else>
                <span
                  v-if="selfUser.name.trim().length"
                  style="color: white; font-size: 14pt"
                  >{{ selfUser.name.split(" ")[0].slice(0, 1)
                  }}{{ selfUser.name.split(" ")[1].slice(0, 1) }}</span
                >
                <span v-else style="color: white; font-size; 14pt;">{{
                  selfUser.username.slice(0, 2).toUpperCase()
                }}</span>
              </v-avatar>
            </v-avatar>
            <v-col>
              <div
                contenteditable="true"
                class="create"
                id="create-post"
                placeholder="¿Deseas anunciar algo?"
                @keyup="AddContent()"
              ></div>
            </v-col>
          </v-row>
          <v-divider class="mt-2 mb-2"></v-divider>

          <v-row v-if="tagUsers" class="pt-0">
            <v-col sm="12">
              <v-form>
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
                    <v-chip v-bind="data.attrs" :input-value="data.selected">
                      <v-avatar left v-if="data.item.profilePicture">
                        <img
                          :src="data.item.profilePicture"
                          :alt="data.item.name"
                        />
                      </v-avatar>
                      <v-avatar left color="secondary" v-else>
                        <span
                          v-if="data.item.name"
                          style="color: white; font-size: 8pt"
                          >{{ data.item.name.split(" ")[0].slice(0, 1)
                          }}{{ data.item.name.split(" ")[1].slice(0, 1) }}</span
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
                      <v-list-item-avatar left v-if="data.item.profilePicture">
                        <img
                          :src="data.item.profilePicture"
                          :alt="data.item.name"
                        />
                      </v-list-item-avatar>
                      <v-list-item-avatar left color="secondary" v-else>
                        <span
                          v-if="data.item.name"
                          style="color: white; font-size: 8pt"
                          >{{ data.item.name.split(" ")[0].slice(0, 1)
                          }}{{ data.item.name.split(" ")[1].slice(0, 1) }}</span
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
              </v-form>
            </v-col>
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
                  <span class="btn-text"> Subir fotos </span>
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
                    color="error"
                    outlined
                    @click="
                      photos = [];
                      files = [];
                    "
                    >Eliminar todas</v-btn
                  >
                  <v-btn
                    class="mr-1"
                    :color="photos.length ? 'accent' : 'primary'"
                    @click="dialog = false"
                  >
                    {{ photos.length ? "Listo" : "Cerrar" }}
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
              <span class="btn-text"> Etiquetar usuarios </span>
              <span v-if="tagUserslist.length"
                >({{ tagUserslist.length }})</span
              >
            </v-btn>
            <v-btn
              :disabled="loading"
              @click="submitPost()"
              color="primary"
              class="ml-auto mr-3 submit-post"
              >Publicar</v-btn
            >
          </v-row>
        </form>
      </v-container>
    </v-card>

    <PubList v-if="!reload" />

    <v-snackbar v-model="snackbar" :timeout="timeout">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" outlined v-bind="attrs" @click="snackbar = false">
          cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState, mapMutations } from "vuex";
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
    attrs: "",
    reload: false,
    api_dir: "/robotarium-api/v1.0/new-post/",
  }),
  computed: {
    ...mapState([
      "users",
      "selfUser",
      "authentication",
      "domainBase",
      "wsBase",
    ]),
  },
  created() {
    document.title = "Inicio · UAO-RAS";
    this.setViewname("Inicio");
  },
  mounted() {
    this.$sse(this.domainBase + "/notifications/", { format: "json" }) // or { format: 'plain' }
      .then((sse) => {
        // Store SSE object at a higher scope
        var msgServer = sse;
        // Catch any errors (ie. lost connections, etc.)
        sse.onError((e) => {
          console.error("lost connection; giving up!", e);

          // This is purely for example; EventSource will automatically
          // attempt to reconnect indefinitely, with no action needed
          // on your part to resubscribe to events once (if) reconnected
          sse.close();
        });

        // Listen for messages without a specified event
        sse.subscribe("notification", (message, rawEvent) => {
          this.reload = true;
          this.sleep(5).then(() => {
            this.reload = false;
          });
        });
      })
      .catch((err) => {
        // When this error is caught, it means the initial connection to the
        // events server failed.  No automatic attempts to reconnect will be made.
        console.error("Failed to connect to server", err);
      });
  },
  methods: {
    ...mapMutations(["setViewname"]),
    AddContent() {
      var divContent = document.getElementById("create-post");
      this.content = divContent.innerText;
    },
    async submitPost() {
      if (this.content.length || this.files.length) {
        this.loading = true;
        const formdata = new FormData();
        formdata.append("username", this.selfUser.username);
        formdata.append("content", this.content);
        formdata.append("num_photos", this.photos.length);
        formdata.append("num_users", this.tagUserslist.length);
        this.files.forEach((file) => {
          formdata.append(`photo_${this.files.indexOf(file)}`, file);
        });
        this.tagUserslist.forEach((user) => {
          formdata.append(`user_${this.tagUserslist.indexOf(user)}`, user);
        });

        const options = {
          method: "POST",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
          },
          body: formdata,
        };
        delete options.headers["Content-Type"];

        let response = await fetch(this.domainBase + this.api_dir, options);
        response = await response.json();
        if (!response.created) {
          this.message =
            "Ha sucedido un error inesperado, intenta de nuevo más tarde.";
          this.snackbar = true;
        } else {
          this.sendNotification();
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
    sendNotification() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";

      this.tagUserslist.forEach((user) => {
        var websocket = new WebSocket(
          protocol + this.wsBase + "/ws/notifications/" + user + "/"
        );
        let sockedData = {
          type: "new_notification",
          sender: this.selfUser.username,
          receiver: user,
        };
        websocket.onopen = () => websocket.send(JSON.stringify(sockedData));
        websocket.onmessage = ({ data }) => {
          websocket.close();
        };
      });
    },
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },
};
</script>

<style scoped>
.create {
  background: rgba(197, 7, 7, 0.1);
  padding: 10px;

  border-radius: 10px;
  width: auto;
  height: auto;
  min-height: 18pt;
  max-height: 100px;
  overflow: auto;
  overflow-x: hidden;
  overflow-wrap: break-word;
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
  position: relative;
  color: #4a4a4a;
  background-color: transparent;
}
.create::-webkit-scrollbar {
  width: 3px; /* Tamaño del scroll en vertical */
  height: 3px; /* Tamaño del scroll en horizontal */
  /* display: none; Ocultar scroll */
}
/* Ponemos un color de fondo y redondeamos las esquinas del thumb */
.create::-webkit-scrollbar-thumb {
  background: #be0707;
  border-radius: 4px;
}
.theme--light.v-divider {
  border-color: #be0707 !important;
}
.submit-post {
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
@media (max-width: 960px) {
  .btn-text {
    display: none;
  }
}
</style>
