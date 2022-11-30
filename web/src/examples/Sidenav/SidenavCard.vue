<template>
  <div
    v-show="this.$store.state.layout !== 'landing'"
    class="card card-plain shadow-none"
    id="sidenavCard"
  >
    <div class="p-3 card-body text-center w-100 pt-0">
      <img
        class="w-50 mx-auto"
        src="@/assets/img/illustrations/icon-documentation.svg"
        alt="sidebar_illustration"
      />
      <h6 class="mb-0 text-dark up">需要幫助嗎？</h6>
      <p class="text-xs font-weight-bold">請參考使用手冊</p>
    </div>
    <a
      href=""
      target="_blank"
      class="mb-3 btn btn-dark btn-sm w-100"
      >使用手冊</a
    >
  </div>
</template>
<script>
import img from "../../assets/img/illustrations/icon-documentation.svg";

export default {
  name: "sidenav-card",
  props: ["textPrimary", "textSecondary", "iconClass"],
  data() {
    return {
      img
    };
  }
};
</script>
