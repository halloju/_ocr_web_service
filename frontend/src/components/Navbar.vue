<template>
<nav class="menu">
  <a href="#" class="logo">
    <img src="@/assets/images/esun-ocr-logo.svg" alt="logo">
    <span><a href="/">Esun.OCR</a></span>
  </a>
  <div class="navbar">
    <Dropdown :img_src="img_src1" title="通用文件識別功能" class="navbar-links"/>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}
.menu {
  display: flex;
  background-color: #077C95;
  height: 6vh;
  width: 100%;
  align-items: center;
  justify-content: flex-start;
  padding: 2px;
}
.logo {
  display: flex;
  align-items: center;
  width: 200px;
  margin-left: 15px;
  margin-right: 15px;
}
.logo span {
  margin-left: 10px;
  margin-bottom: 5px;
  color: white;
  font-weight: bold;
  font-size: 1.7rem;
}
.navbar {
  display: flex;
  flex: auto;
  justify-content: flex-end;
}
.navbar img {
  max-width: 30px;
}
.navbar-links  {
  display: flex;
  justify-content: center;
  height: 48px;
  font-weight: bold;
  font-size: 1.2rem;
  margin-left: 5px;
  margin-right: 5px;
}
nav .menu-item {
  color: #FFF;
  padding: 7px 20px;
  position: relative;
  text-align: center;
  border-bottom: 3px solid transparent;
  display: flex;
  transition: 0.4s;
  background-color: #077C95;
}
nav .menu-item.active,
nav .menu-item:hover {
  background-color: #444;
  border-bottom-color: #FF5858;
}
nav .menu-item a {
  color: inherit;
  text-decoration: none;
}
@media (max-width: 980px) {
  .menu {
    min-width: 768px;
  }
  .navbar .menu-item {
    justify-content: left;
    font-size: 1.3rem;
  }
  .navbar-links {
    justify-content: flex-end;
    width: 100%;
    text-align: center;
  }
  .navbar-links .menu-title {
    display: none;
  }
  .navbar-links:hover {
    background-color: #578F8D;
  }
  .menu {
    justify-content: space-between;
  }
}
</style>