<template>
    <div>
        <WebSocketLive number="" />
    </div>
</template>

<script>
import {mapMutations} from "vuex";
import WebSocketLive from "@/components/subcomponents/WebSocketLive.vue";
export default {
    name: "RobotVideoStream",
    data: ()=>({
        websocket_dir: '',
    }),
    components:{
        WebSocketLive,
    },
    created(){
        let robotariumInfo = {
            robot: 'Duckiebot1'
        }
        this.setRobotariumInfo(robotariumInfo)
    },
    methods:{
        ...mapMutations(["setRobotariumInfo"])
    }
}
</script>