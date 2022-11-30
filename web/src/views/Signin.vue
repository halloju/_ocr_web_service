<template>
  <main class="mt-0 main-content">
    <section>
      <div class="page-header min-vh-100">
        <div class="container">
          <div class="row">
            <div class="mx-auto col-xl-4 col-lg-5 col-md-7 d-flex flex-column mx-lg-0">
              <div class="card card-plain">
                <div class="pb-0 card-header text-start">
                  <h4 class="font-weight-bolder">登入</h4>
                  <p class="mb-0">請輸入您的帳號與密碼</p>
                </div>
                <div class="card-body">
                  <form role="form">
                    <div class="mb-3">
                      <argon-input type="email" placeholder="帳號" name="email" size="lg" />
                    </div>
                    <div class="mb-3">
                      <argon-input type="password" placeholder="密碼" name="password" size="lg" />
                    </div>
                    <argon-switch id="rememberMe">記住我</argon-switch>

                    <div class="text-center">
                      <argon-button
                        @button-click="login"
                        class="mt-4"
                        variant="gradient"
                        color="success"
                        fullWidth
                        size="lg"
                      >登入</argon-button>
                    </div>
                  </form>
                </div>
                <div class="px-1 pt-0 text-center card-footer px-lg-2">
                  <p class="mx-auto mb-4 text-sm">
                    沒有帳號嗎？
                    <a
                      href="javascript:;"
                      class="text-success text-gradient font-weight-bold"
                    >註冊</a>
                  </p>
                </div>
              </div>
            </div>
            <div
              class="top-0 my-auto text-center col-6 d-lg-flex d-none h-100 pe-0 position-absolute end-0 justify-content-center flex-column"
            >
              <div class="signin-intro position-relative bg-gradient-primary h-100 m-3 px-7 border-radius-lg d-flex flex-column justify-content-center overflow-hidden">
                <span class="mask bg-gradient-success opacity-6"></span>
                <h2 class="mt-5 text-white font-weight-bolder position-relative">玉山智能辨識系統</h2>
                <h4 class="mt-5 text-white font-weight-bolder position-relative">絕對是您最佳的工作夥伴</h4>
                <p
                  class="text-white position-relative"
                >介面好用、辨識好準、效率好棒</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
<style scoped>
@import '../assets/css/signin.css';
</style>
<script>
import ArgonInput from "@/components/ArgonInput.vue";
import ArgonSwitch from "@/components/ArgonSwitch.vue";
import ArgonButton from "@/components/ArgonButton.vue";
const body = document.getElementsByTagName("body")[0];

export default {
  name: "signin",
  components: {
    ArgonInput,
    ArgonSwitch,
    ArgonButton,
  },
  created() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
    body.classList.remove("bg-gray-100");
  },
  beforeUnmount() {
    this.$store.state.hideConfigButton = true;
    this.$store.state.showNavbar = false;
    this.$store.state.showSidenav = false;
    this.$store.state.showFooter = false;
    body.classList.add("bg-gray-100");
  },
  methods: {
    login() {
      console.log('hi')
      this.$router.push({ path: `/dashboard-default` });
    }
  }
};
</script>
