<template>
<div>
<Stand class="pa-0" stand="A" levels="5" />
        <Stand class="mt-4 pa-0" stand="B" levels="6" />
</div>
 
</template>

<script>

import Stand from "@/components/Stand.vue";
export default {
    name:"Reservation",
    components:{
    
        Stand
    },
    created(){
        document.title = "Inventario · UAO-RAS"
        
    },
}
</script>

<style>

</style>