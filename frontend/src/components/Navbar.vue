<template>
<nav class="menu">
  <a href="#" class="logo">
    <img src="https://static.overlay-tech.com/assets/a29acb82-a927-42fa-ba0a-59c8194dc5bb.svg" alt="logo">
    <span>Esun.OCR</span>
  </a>
  <div class="navbar">
    <Dropdown :img_src="img_src1" title="通用文件識別功能" class="navbar-links"/>
    <Dropdown :img_src="img_src2" title="自定義模板" :items="services2" class="navbar-links"/>
    <Dropdown :img_src="img_src3" title="特殊文件識別功能" :items="services3" class="navbar-links"/>
  </div>
  <div class="user">
    <div class="group-circle">
      <div class="user-icon"></div>
    </div>
    <div class="relative-wrapper-one">
      <p class="esb">ESB22005</p>
      <p class="admin-account">Admin account</p>
    </div>
  </div>
  <div class="navbar-toggle">
      <i class="fa fas fa-bars"></i>
  </div>
</nav>
</template>

<script>
import Dropdown from '../components/Dropdown.vue';
export default {
name: 'navbar',
components: {
  Dropdown
},
data () {
  return {
    img_src1: 'https://static.overlay-tech.com/assets/0c80f190-377f-45a2-a5ce-e120498cbfad.svg',
    img_src2: 'https://static.overlay-tech.com/assets/57ef4a3c-d5fc-4a5f-888d-01e66bce4afb.svg',
    img_src3: 'https://static.overlay-tech.com/assets/687cd02f-3a17-4439-8274-a745fff98f94.svg',
    services2: [
      {
        title: '新增自定義模板',
        link: '#',
        img_src: '',
      },
      {
        title: '模板列表',
        link:'#'
      },
      {
        title: '模板辨識',
        link: '#'
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
  height: 48px;
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
  max-width: 27px;
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
.user {
  width: 180px;
  display: flex;
  align-items: center;
}
.group-circle {
  background-color: #FFC145;
  margin-right: 10px;
  border-radius: 50%;
  padding: 3px 3px 3px 3px;
  display: flex;
  align-items: center;
  width: 30px;
  height: 30px;
}
.user-icon {
  background-size: 100% 100%;
  background-position: center;
  background-image: url("https://static.overlay-tech.com/assets/cbffd0be-e5e1-4257-9b0c-93d9640e17bd.svg");
  padding: 8px 11px;
  display: flex;
  justify-content: center;
}
.relative-wrapper-one p {
  color: white;
  font-weight: bold;
}
.navbar-toggle {
  display: none;
}

nav .menu-item {
  color: #FFF;
  padding: 10px 20px;
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
@media (max-width: 1080px) {
  .navbar img {
    max-width: 20px;
  }
  .navbar-links  {
    justify-content: flex-end;
    height: 48px;
    font-size: 1rem;
    margin-left: 3px;
    margin-right: 3px;
  }
}
@media (max-width: 980px) {
  .navbar {
    position: absolute;
    top: 48px;
    right: 0%;
    width: 270px;
    height: 30xvh;
    background-color: #008b8b;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    border-radius: 10px;
  }
  .navbar li {
    display: flex;
    margin: 30px 0;
    padding: 0px 25px;
  }
  .navbar-links {
    width: 100%;
    text-align: center;
  }
  .navbar-links:hover {
  background-color: #578F8D;
  }
  .fa {
    color: white;
  }
  .navbar-toggle {
    display: flex;
    font-size: 35px;
  }
  .user {
    width: 200px;
    display: flex;
    justify-content: center;
  }
}
</style>