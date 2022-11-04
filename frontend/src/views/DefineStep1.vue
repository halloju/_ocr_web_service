<template>
  <div class="step">
    Step 1. 上傳範例圖片
  </div>
  <DropAnImage />
  <div class="buttons">
    <router-link to="/define/step2" class="btn bg-orange">➡ 下一步</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
import DropAnImage from '@/components/DropAnImage.vue'
export default {
  name: 'DefineStep1',
  components: {
    DropAnImage
  },
  data() {
    return {

    };
  },
  methods: {
      
    }

};
</script>