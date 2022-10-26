<template>

</template>

<style scoped>
@import '../assets/css/home.css';
</style>
<script>
export default {
  data() {
    return {

    };
  },
  methods: {
      home() {
          this.$store.commit('back');
      }
    }

};
</script>