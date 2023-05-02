<script>
export default {
    components: {},
    name: 'Login',
    data() {
        return {
            account: '',
            password: '',
            checked: false
        };
    },
    methods: {
        login() {
            this.$router.push({ path: '/home' });
        }
    }
};
</script>
<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img src="@/assets/img/esun_logo.svg" alt="Image" height="50" class="mb-3" />
                        <div class="text-900 text-3xl font-medium mb-3">智能辨識系統</div>
                        <span class="text-600 font-medium">歡迎使用</span>
                    </div>

                    <div>
                        <label for="account1" class="block text-900 text-xl font-medium mb-2">帳號</label>
                        <InputText id="account1" type="text" placeholder="請您輸入帳號" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="account" />

                        <label for="password1" class="block text-900 font-medium text-xl mb-2">密碼</label>
                        <Password id="password1" v-model="password" placeholder="請您輸入密碼" :toggleMask="true" class="w-full mb-3" inputClass="w-full" inputStyle="padding:1rem"></Password>

                        <div class="flex align-items-center justify-content-between mb-5 gap-5">
                            <div class="flex align-items-center">
                                <Checkbox v-model="checked" id="rememberme1" binary class="mr-2"></Checkbox>
                                <label for="rememberme1">記住帳密</label>
                            </div>
                            <a class="font-medium no-underline ml-2 text-right cursor-pointer" style="color: var(--primary-color)">忘記密碼?</a>
                        </div>
                        <Button label="登入" class="w-full p-3 text-xl" @click="login"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}
</style>
