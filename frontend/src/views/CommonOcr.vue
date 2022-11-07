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
@import '@/assets/css/sidebar_frame.css';
</style>
<script>
import feature1 from '@/assets/images/feature1.svg'
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
            model: "通用辨識",
            img_src: feature1,
            model_bar: [{title: "1. 圖片上傳", path: "/common-ocr/upload", sub_title: "圖檔上傳", order: 1},
                        {title: "2. 單張確認", path: "/common-ocr/confirm", sub_title: "圖檔確認", order: 2},
                       ],
      };
  },
  methods: {
    }

};
</script>