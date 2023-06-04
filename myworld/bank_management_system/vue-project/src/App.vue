<template>
  <el-container>
    <el-header><app-header/></el-header>
    <el-main style="margin: 25px"><router-view/></el-main>
  </el-container>
</template>

<script>
import Header from "@/components/Header";

export default {
  name: 'App',
  components: {
    Header,
  },
  computed: {
    isHome() {
      return this.$route.name in window
    }
  }
};
</script>