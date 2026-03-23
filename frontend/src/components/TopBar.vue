<template>
  <header class="topbar">
    <button v-if="back" class="back-btn" @click="$emit('back')">‹</button>
    <h1 class="title">{{ title }}</h1>
    <button v-if="!back" class="refresh-btn" @click="$emit('refresh')">↻</button>
  </header>
</template>

<script setup>
defineProps({ title: String, back: Boolean })
defineEmits(['back', 'refresh'])
</script>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  padding: 16px;
  background: white;
  border-bottom: 1px solid var(--gray-200);
  position: sticky;
  top: 0;
  z-index: 10;
}
.title { flex: 1; font-size: 18px; font-weight: 700; text-align: center; }
.back-btn, .refresh-btn {
  width: 36px; height: 36px;
  border: none; background: var(--gray-100);
  border-radius: 50%; font-size: 20px;
  cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.back-btn { font-size: 24px; font-weight: 300; }
</style>
