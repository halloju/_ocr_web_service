<template>
  <Navbar />
  <div class="dashboard">
      <Sidebar :model="model" :img_src="img_src" :model_bar="model_bar"/>
      <div class="content">
          <router-view></router-view>
      </div>
  </div>
</template>
<style scoped>
@import '@/assets/css/sidebar.css';
</style>
<script>
import feature2 from '@/assets/images/feature2.svg'
import Navbar from '../components/Navbar.vue'
import Sidebar from '../components/Sidebar.vue'
export default {
  components: {
    Navbar,
    Sidebar,
  },
  name: 'Define',
  data() {
    return {
            model: "新增自定義模板",
            img_src: feature2,
            model_bar: [{title: "1. 範例圖檔上傳", path: "/define/step1", sub_title: "Step 1", order: 1},
                        {title: "2. 文字位置標註", path: "/define/step2", sub_title: "Step 2", order: 2},
                        {title: "3. 方塊位置標註", path: "/define/step3", sub_title: "Step 3", order: 3},
                        {title: "4. Mask 位置標註", path: "/define/step4", sub_title: "Step 4", order: 4},
                        {title: "5. 資訊確認", path: "/define/step5", sub_title: "Step 5", order: 5}],
    };
  },
  methods: {
    }

};
</script>