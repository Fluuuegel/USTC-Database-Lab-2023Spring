<template>
  <el-container>
    <el-header v-if="isHome"><app-header/></el-header>
    <el-main style="margin: 0px"><router-view/></el-main>
  </el-container>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: 'App',
  components: {
    AppHeader,
  },
  computed: {
    isHome() {
      // console.log(this.$route.path); 
      return this.$route.path.indexOf('/admin/') === 0;
    }
  }
};
</script>