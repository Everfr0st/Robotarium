<template>
    <div>
        <v-chip class="ma-1"  link  color="primary">
            <v-avatar left color="secondary" @mouseenter="active=true;" @mouseleave="active=false;">
            <img v-if="tagUser.profilePicture" :src="tagUser.profilePicture" :alt="tagUser.name?tagUser.name:'@'+tagUser.username" />
            <span v-else style="color: white; font-size: 8pt;">
                {{tagUser.name.trim().length?tagUser.name.trim().slice(0, 1)+tagUser.name.trim().split(" ")[1].slice(0, 1):tagUser.username.toUpperCase().slice(0,2)}}
            </span>
          </v-avatar>
          <span>
            {{tagUser.name.trim().length?tagUser.name:'@'+tagUser.username}}
            </span>
          </v-chip>
    </div>  
</template>

<script>
import {mapState} from "vuex";
export default {
    data: () => ({
        tagUser: '',

    }),
    props: ["user"],
    computed:{
        ...mapState(["users"])
    },
    created(){
        for(let i = 0; i < this.users.length; i++){
            if (this.users[i].username.indexOf(this.user) > -1) {
            this.tagUser = this.users[i];
          } 
        }
    },
}
</script>