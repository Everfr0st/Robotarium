<template>
    <div>
        <Stand class="pa-0" stand="A" levels="5" />
        <Stand class="mt-4 pa-0" stand="B" levels="6" />
<Reservation/>
    </div>
</template>

<script>
import Stand from "@/components/Stand.vue";
import Reservation from "@/components/Reservation.vue"
import {mapMutations} from "vuex";
import Reservation from '../components/Reservation.vue';
export default {
    name: "Inventory",
    components:{
        Reservation,
        Stand
    },
    created(){
        document.title = "Inventario · UAO-RAS"
        this.setViewname("Inventario");
    },
    methods:{
        ...mapMutations(["setViewname"])
    }
}
</script>