<template>
  <img
    v-if="config.brandLogo"
    :src="config.brandLogo"
    alt="WTF Support"
    class="h-8 w-8 shrink-0 object-cover"
  />
  <WTFLogo v-else class="h-8 w-8 shrink-0 rounded" />
</template>

<script setup lang="ts">
import WTFLogo from "@/assets/logos/WTFLogo.vue";

import { useConfigStore } from "@/stores/config";
const config = useConfigStore();
</script>

<style scoped></style>
