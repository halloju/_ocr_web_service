<template>
  <div id="app">
    <Navbar />
    <div class="dashboard">
        <Sidebar/>
        <div class="content">
            <router-view/>
        </div>
    </div>
  </div>
</template>

<style>
@import './assets/css/base.css';
@import './assets/css/common.css';
.dashboard {
    display: grid;
    grid-template-columns: 1fr 5fr;
    background-color: #10A0A7;
    height: 90vh;
    width: 100vw;
}
.content {
    background: url('@/assets/images/dashborad-bg.svg') no-repeat;
    background-size: 130%;
    background-position: bottom;
    background-color: #09747A;
    border-radius: 0px;
    height: 100%;
}
</style>

<script>
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'

export default {
  components: {
    Navbar,
    Sidebar,
  },
  data() {
    return {
    }
  }
}
</script>