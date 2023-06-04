<template>
    <el-menu router mode="horizontal" :default-active="$route.path">
      <el-menu-item index="/staff">客户管理</el-menu-item>
      <el-submenu index="">
        <template #title>账户管理</template>
        <el-menu-item index="/account">账户</el-menu-item>
      </el-submenu>
      <el-menu-item index="/loan">贷款管理</el-menu-item>
      <el-menu-item index="/statistics">业务统计</el-menu-item>
    </el-menu>
  </template>
  
  <script>
  export default {
    name: "Header"
  }
  </script>