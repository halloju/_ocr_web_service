<template>
  <div class="step">
    Step 4. 編輯遮罩：遮住會變動區域
  </div>
  <div class="contentWrapperFlex">
    <Box 
      :boxName="boxName"
      :fillColor="fillColor"
    />
    <BoxCard
      :boxName="boxName"
      :boxTitle="boxTitle"
    />
  </div>
  <div class="buttons">
    <router-link to="/define/step5" class="btn bg-primary"><i class="fa fa-save">&nbsp;&nbsp;</i>完成</router-link>
  </div>
</template>

<style scoped>
@import '@/assets/css/content.css';
</style>
<script>
import Box from '@/components/Box.vue'
import BoxCard from '@/components/BoxCard.vue'
export default {
  name: 'DefineStep4',
  components: {
    Box,
    BoxCard
  },
  data() {
    return {
      boxName: 'recs_mask',
      boxTitle: '遮罩位置',
      fillColor: 'rgba(0, 0, 0, 0.5)'
    };
  },
  methods: {
    }

};
</script>