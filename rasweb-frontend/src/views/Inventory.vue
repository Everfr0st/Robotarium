<template>
    <div>
        <Stand stand="A" levels="5" />
        <Stand class="mt-4" stand="B" levels="6" />

    </div>
</template>

<script>
import Stand from "@/components/Stand.vue";

export default {
    name: "Inventory",
    components:{
        Stand
    },
    created(){
        document.title = "Inventario · UAO-RAS"
    }
}
</script>