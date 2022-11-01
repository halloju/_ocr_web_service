<template>
  <div id="app">
    <Navbar />
    <div class="main">
        <router-view></router-view>
    </div>
  </div>
</template>

<style>
@import './assets/css/base.css';
@import './assets/css/common.css';

</style>

<script>
import Navbar from './components/Navbar.vue'

export default {
  components: {
    Navbar,
  },
  data() {
    return {
    }
  }
}
</script>