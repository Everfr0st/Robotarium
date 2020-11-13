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
                post.name.trim().length ? post.name.slice(0, 1).toUpperCase() + post.name.split(" ")[1].slice(0, 1).toUpperCase() : post.username.slice(0, 2).toUpperCase()
              }}</span>
            </v-avatar>
            <p :title="post.name" v-if="post.name.trim().length" class="ml-3">
              {{ post.name }}
            </p>
            <p :title="'@'+post.username" :class="post.name.trim().length? 'ml-1':'ml-3'" style="color: grey; font-size: 14pt">@{{ post.username }}</p>
          </v-card-title>
          <v-card-subtitle
            style="
              position: absolute;
              left: 35px;
              bottom: -15px;
              font-size: 9pt;
            "
          >
            <v-icon size="15">mdi-progress-clock</v-icon>
            <span :title="post.created">

            {{ post.created }}
            </span>
          </v-card-subtitle>
        </v-row>
        <v-row>
          <v-card-text style="padding: 0px; font-size: 12pt;">
            {{ post.content }}
          </v-card-text>
          <v-card-actions class="pa-0 mt-1">
              <v-icon size="30" color="accent" class="mr-1">mdi-account-supervisor</v-icon>    
              <UserInTag v-for="(tag_user, index) in post.tag_users" :key="index" :user="tag_user" />
          </v-card-actions>
        </v-row>
        <v-row class="pr-7 mt-2" >
          <v-carousel :continuous="false" style="border-radius: 5px; z-index: 0;">
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
import UserInTag from "@/components/subcomponents/UserInTag.vue";

export default {
  name: "PubList",
  data: () => ({
    api_dir: "/robotarium-api/v1.0/post-list/",
    posts: [],
    loading: true,
  }),
  components: {
    UserInTag
  },
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
    }
  },
};
</script>