<template>
  <div class="step">
    Step 3. 標註要項位置
  </div>
  <div class="contentWrapperFlex">
    <Box 
      :boxName="boxName"
    />
    <BoxCard
      :boxName="boxName"
      :BoxTitle="BoxTitle"
    />
  </div>
  <div class="buttons">
    <router-link to="/define/step4" class="btn bg-primary">➡ 下一步</router-link>
    <router-link to="" class="btn bg-orange btn-right">⬆ 上傳設定檔</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>

<script>
import Box from '@/components/Box.vue';
import BoxCard from '@/components/BoxCard.vue';

export default {
  name: 'DefineStep3',
  components: {
    BoxCard,
    Box,
  },
  data() {
    return {
      boxName: 'recs_block',
      BoxTitle: '核取方塊位置',
    };
  },
};
</script>