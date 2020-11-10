<template>
    <div>
        <h1>Inventario</h1>
        <Stand stand="A"/>
        <Stand stand="B"/>
    </div>
</template>

<script>
import Stand from "@/components/Stand.vue";

export default {
    components:{
        Stand
    },
    created(){
        document.title = "Inventario · UAO-RAS"
    }
}
</script>