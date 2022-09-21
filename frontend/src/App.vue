<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
export default {
  components: {
    Header,
    Footer
  },
  data() {
    return {
      floor:''
    }
  }
}
</script>

<template>
  <div id="app">
    <Header />
    <section class="bg py-5">
      <router-view></router-view>
      <!-- <LineTabs :tabs="tabs"/> -->
    </section>
    <Footer />
  </div>
</template>

<style>
@import './assets/css/base.css';
@import './assets/css/common.css';
</style>