<script setup>
import ChatBox from './components/ChatBox.vue'
</script>

<template>
  <div class="app-container">
    <ChatBox />
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>
