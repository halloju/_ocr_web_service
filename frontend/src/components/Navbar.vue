<template>
<nav class="menu">
  <a href="#" class="logo">
    <img src="@/assets/images/esun-ocr-logo.svg" alt="logo">
    <span><a href="/">Esun.OCR</a></span>
  </a>
  <div class="navbar">
    <Dropdown :img_src="img_src1" title="通用文件識別功能" :items="services1" class="navbar-links"/>
    <Dropdown :img_src="img_src2" title="自定義模板" :items="services2" class="navbar-links"/>
    <Dropdown :img_src="img_src3" title="特殊文件識別功能" :items="services3" class="navbar-links"/>
    <Dropdown :img_src="img_src4" title="ESB18507" :items="user_info" class="navbar-links"/>
  </div>
</nav>
</template>

<script>
import Dropdown from '../components/Dropdown.vue';
import user_icon from '@/assets/images/user-icon.svg'
import feature1 from '@/assets/images/feature1.svg'
import feature2 from '@/assets/images/feature2.svg'
import feature3 from '@/assets/images/feature3.svg'

export default {
name: 'navbar',
components: {
  Dropdown
},
data () {
  return {
    img_src1: feature1,
    img_src2: feature2,
    img_src3: feature3,
    img_src4: user_icon,
    services1: [
      {
        title: '通用辨識',
        link: '/common-ocr',
        img_src: '',
      },
    ],
    services2: [
      {
        title: '新增自定義模板',
        link: '/define',
        img_src: '',
      },
      {
        title: '模板列表',
        link:'/template-list'
      },
      {
        title: '模板辨識',
        link: '/template-ocr'
      }
    ],
    services3: [
      {
        title: '身份證辨識',
        link: '#',
        img_src: '',
      },
      {
        title: '第二證件辨識',
        link:'#'
      },
      {
        title: '存摺辨識',
        link: '#'
      }
    ],
    user_info: [
      {
        title: '登出',
        link: '/login',
      }
    ]
  }
}
}
</script>

<style>
@import '@/assets/css/navbar.css';
</style>