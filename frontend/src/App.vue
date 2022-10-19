<template>
    <center>
        <h1>Cock!!</h1>
        <input id="no" type="text" name="idk" v-model="idk">
        <button v-on:click="add_user()">Gi!</button>
    </center>   
</template>

<script>

export default {
    name: "app",
    data() {
        return {
            idk: ""
        }
    },
    methods: {
        add_user() {
            const h1 = document.createElement("h1")
            h1.innerHTML = this.idk
            console.log(h1)
            const query = document.querySelector("center")
            query.bodappendChild(h1)
        },
    },
};



</script>