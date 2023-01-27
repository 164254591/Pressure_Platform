<template>
  <div>
    <span>欢迎来到首页,{{username}}</span>
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