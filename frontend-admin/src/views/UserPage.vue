<template>
  <el-card>
    <el-table :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="hsk_level" label="HSK等级" />
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
const users = ref([
  { id: 1, username: 'admin', email: 'admin@test.com', hsk_level: 6 },
  { id: 2, username: 'test', email: 'test@test.com', hsk_level: 3 }
]);
</script> 