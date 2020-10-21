<template>
  <div class="ml-6">
    <v-lazy
      transition="fade-transition"
      :options="{ threshold: 0.5 }"
      v-for="(post, index) in posts"
      :key="index"
    >
      <v-card elevation="0">
        <v-row
          wrap
          justify="start"
          class="pa-0"
          align="center"
          style="position: relative"
        >
          <v-card-title style="padding: 0px">
            <v-avatar size="40" color="secondary">
              <img
                v-if="post.profile_picture"
                :src="domain_base + post.profile_picture"
                :alt="post.name ? post.name : '@' + post.username"
              />
              <span style="color: white" v-else>{{
                post.name ? post.name.slice(0, 1) : post.username.slice(0, 1)
              }}</span>
            </v-avatar>
            <p class="ml-3 mr-1">
              {{ post.name }}
            </p>
            <p style="color: grey; font-size: 14pt">@{{ post.username }}</p>
          </v-card-title>
          <v-card-subtitle
            style="
              position: absolute;
              left: 35px;
              bottom: -12px;
              font-size: 9pt;
            "
          >
            <v-icon size="15">mdi-progress-clock</v-icon>
            {{ post.created }}
          </v-card-subtitle>
        </v-row>
        <v-row>
          <v-card-text style="padding: 0px">
            {{ post.content }}
            <p v-if="post.tag_users.length">
              Con
              <a
                color="accent"
                text
                v-for="(tag_user, index) in post.tag_users"
                :key="index"
              >
                @{{ tag_user
                }}<span v-if="index < post.tag_users.length - 1">,</span>
              </a>
            </p>
          </v-card-text>
        </v-row>
        <v-row class="pr-7" >
          <v-carousel style="border-radius: 5px; z-index: 0;">
            <v-carousel-item
              v-for="(photo, index) in post.photos"
              :key="index"
              :src="`${domain_base}/coco-files/${photo}`"
              reverse-transition="fade-transition"
              transition="fade-transition"
            ></v-carousel-item>
          </v-carousel>
        </v-row>

        <v-row class="pr-7">
          <v-divider class="mt-2 mb-2"></v-divider>
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
export default {
  name: "PubList",
  data: () => ({
    api_dir: "/coco-api/v1.0/post-list/",
    posts: [],
    loading: true,
  }),
  computed: {
    ...mapState(["authentication", "domain_base"]),
  },
  async created() {
    let response = await fetch(this.domain_base + this.api_dir, {
      method: "GET", // *GET, POST, PUT, DELETE, etc.
      headers: {
        Authorization: `Bearer ${this.authentication.accessToken}`,
      },
    });

    if (response.status == 200) {
      response = await response.json();
      this.posts = response;
      this.loading = false;
      console.log(this.posts);
    }
  },
};
</script>