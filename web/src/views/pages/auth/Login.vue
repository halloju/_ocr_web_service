<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { SSO_URL, LOGIN_URL } from '@/url.js';
export default {
    components: {},
    name: 'Login',
    data() {
        return {
            checked: false
        };
    },
    mounted() {
        axios
            .get(SSO_URL)
            .then((res) => {
                const re_url = res.data;
                if (re_url) window.location.replace(re_url);
                else this.$router.push({ path: '/home' });
            })
            .catch((err) => {
                console.log(err);
            });
    },
    setup() {
        ElMessage('頁面跳轉中');
    },
    methods: {
        login() {
            axios
                .get(LOGIN_URL)
                .then((res) => {
                    this.$router.push({ path: '/home' });
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        isValidAdfsRedirectUrl(url) {
            try {
                // Parse the URL
                const parsedUrl = new URL(url);

                // Check for specific domain
                const isValidDomain = parsedUrl.hostname === 'adfs.esunbank.com.tw' || parsedUrl.hostname === 'sts.testesunbank.com.tw';

                // Check for specific path 
                const isValidPath = parsedUrl.pathname.startsWith('/adfs/ls/');

                // Check for necessary query parameters
                const hasRequiredParams = parsedUrl.searchParams.has('SAMLRequest');

                return isValidDomain && isValidPath && hasRequiredParams;
            } catch (e) {
                // If URL parsing fails, the URL is not valid
                return false;
            }
        }
    }
};
</script>

<!-- <template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                    <div class="text-center mb-5">
                        <img src="@/assets/img/esun_logo.svg" alt="Image" height="50" class="mb-3" />
                        <div class="text-900 text-3xl font-medium mb-3">智能OCR服務</div>
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
</template> -->

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
