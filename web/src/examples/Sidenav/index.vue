<template>
  <div
    v-show="this.$store.state.layout === 'default'"
    class="min-height-300 position-absolute w-100"
    :class="`${this.$store.state.darkMode ? 'bg-transparent' : 'bg-success'}`"
  />
  <div
    class="my-3 overflow-auto border-0 sidenav navbar navbar-vertical navbar-expand-xs border-radius-xl fixed-start ms-3"
    :class="` 
    ${
      this.$store.state.layout === 'landing'
        ? 'bg-transparent shadow-none'
        : ' '
    } ${this.$store.state.sidebarType}`"
    id="sidenav-main"
  >
    <div class="sidebar">
      <div class="sidenav-header">
        <i
          class="top-0 p-3 cursor-pointer fas fa-times text-secondary opacity-5 position-absolute end-0 d-none d-xl-none"
          aria-hidden="true"
          id="iconSidenav"
        ></i>
        <router-link class="m-0 navbar-brand" to="/">
          <img
            :src="
              this.$store.state.darkMode ||
              this.$store.state.sidebarType === 'bg-default'
                ? logoWhite
                : logo
            "
            class="navbar-brand-img h-100"
            alt="main_logo"
          />
          <span class="sidebar-title ms-2 me-2">Esun.OCR</span>
        </router-link>
      </div>
      <hr class="mt-0 horizontal dark" />
      <sidenav-list :cardBg="custom_class" />
    </div>
  </div>
</template>
<style>
/* .sidebar {
  background-color: #10A0A7;
} */
.sidebar-title {
  font-weight: bold;
  font-size: 22px;
}
</style>
<script>
import SidenavList from "./SidenavList.vue";
import logo from "@/assets/images/esun-ocr-logo.svg";
import logoWhite from "@/assets/images/esun-ocr-logo.svg";

export default {
  name: "index",
  components: {
    SidenavList
  },
  data() {
    return {
      logo,
      logoWhite
    };
  },
  props: ["custom_class", "layout"]
};
</script>
