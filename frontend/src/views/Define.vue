<template>
  <Navbar />
  <div class="dashboard">
      <Sidebar/>
      <div class="content">
          <router-view></router-view>
      </div>
  </div>
</template>
<style scoped>
.dashboard {
    display: grid;
    grid-template-columns: 1fr 5fr;
    background-color: #10A0A7;
    height: 94vh;
    width: 100vw;
}
.content {
    background: url('@/assets/images/dashborad-bg.svg') no-repeat;
    background-size: 130%;
    background-position: bottom;
    background-color: #09747A;
    border-radius: 0px;
    height: 94vh;
}
</style>
<script>
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

    };
  },
  methods: {
    }

};
</script>