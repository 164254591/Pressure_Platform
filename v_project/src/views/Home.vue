<template>
  <div>
    <h2>欢迎来到首页,{{username}}</h2>
  </div>
</template>

<script>
export default {
  name: "Home",
  data(){
    return{
      username:'',
    }
  },
  mounted() {
    this.username=sessionStorage.getItem('username')
  }
}
</script>

<style scoped>

</style>