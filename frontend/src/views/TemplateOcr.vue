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
            model: "模板辨識",
            img_src: feature2,
            model_bar: [{title: "1. 圖檔上傳", path: "/template-ocr/upload", sub_title: "1. 圖檔上傳"},
                      ],
      };
  },
  methods: {
    }

};
</script>