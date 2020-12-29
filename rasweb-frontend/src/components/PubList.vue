<template>
  <div>
    <v-lazy
      transition="fade-transition"
      :options="{ threshold: 1 }"
      v-for="(post, index) in posts"
      :key="index"
    >
      <v-card class="mx-4" elevation="0">
          <v-card-title class="ma-0 pa-0">
            <v-list-item class="pa-0" two-line>
              <v-list-item-avatar color="secondary">
                <img
                  v-if="post.profilePicture"
                  :src="domainBase + post.profilePicture"
                  :alt="post.name ? post.name : '@' + post.username"
                />
                <span style="color: white " v-else>{{
                  post.name.trim().length
                    ? post.name.slice(0, 1).toUpperCase() +
                      post.name.split(" ")[1].slice(0, 1).toUpperCase()
                    : post.username.slice(0, 2).toUpperCase()
                }}</span>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title :title="post.name">
                  <span>
                  {{ post.name }}
                  </span>
                  <span class="username" :title="'@'+ post.username"> @{{ post.username }}</span></v-list-item-title
                >
                <v-list-item-subtitle :title="'@' + post.username"
                  ><v-icon size="15">mdi-progress-clock</v-icon>
                  <span :title="post.created">
                    <small>
                      {{ post.created }}
                    </small>
                  </span></v-list-item-subtitle
                >
              </v-list-item-content>
            </v-list-item>
          </v-card-title>
          <v-card-text class="secondary--text" style="padding: 0px; font-size: 14pt">
            {{ post.content }}
          </v-card-text>
          <v-card-actions v-if="users.length" class="pa-0 mt-1">
            <v-icon v-if="post.tag_users.length" size="30" color="secondary" class="mr-1"
              >mdi-account-supervisor</v-icon
            >
            <UserInTag
              v-for="(tag_user, index) in post.tag_users"
              :key="index"
              :user="tag_user"
            />
          </v-card-actions>
          <v-carousel
            :continuous="false"
            v-if="post.photos.length"
            class="carousel-pub-list mt-2"
            style="border-radius: 5px"
          >
            <v-carousel-item
              v-for="(photo, index) in post.photos"
              :key="index"
              :src="`${domainBase}/ras-uao-files/${photo}`"
              reverse-transition="fade-transition"
              transition="fade-transition"
            >
            </v-carousel-item>
          </v-carousel>
        <v-row class="pr-3">
          <v-divider class="ml-3 mb-3 mt-3"></v-divider>
        </v-row>
      </v-card>
    </v-lazy>
    <v-skeleton-loader
      v-if="loading"
      type="list-item-avatar, image"
    ></v-skeleton-loader>
  </div>
</template>

<script>
import { mapState } from "vuex";
import UserInTag from "@/components/subcomponents/UserInTag.vue";

export default {
  name: "PubList",
  data: () => ({
    api_dir: "/robotarium-api/v1.0/post-list/",
    posts: [],
    loading: true,
  }),
  components: {
    UserInTag,
  },
  computed: {
    ...mapState(["authentication", "domainBase", "users"]),
  },
  async created() {
    let response = await fetch(this.domainBase + this.api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Token ${this.authentication.accessToken}`,
      },
    });
    if (response.status == 200) {
      response = await response.json();
      this.posts = response;
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.v-image__image {
  height: auto;
}
.username{
  color: rgb(133, 133, 133);
}
</style>