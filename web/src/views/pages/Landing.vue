<script>
import axios from 'axios';
import logo from '@/assets/img/esun-ocr-logo.svg';
export default {
    name: 'landing',
    data() {
        return {
            logoUrl: logo,
            version: import.meta.env.VITE_APP_VERSION,
            isHovered: {},
            loggedIn: false
        };
    },
    methods: {
        goLogin() {
            this.$router.push({ path: '/auth/login' });
        },
        smoothScroll(id) {
            document.querySelector(id).scrollIntoView({
                behavior: 'smooth'
            });
        },
        over(id) {
            this.isHovered[id] = true;
        },
        leave(id) {
            this.isHovered[id] = false;
        },
        goToPage(page) {
            this.$router.push({ path: page });
        },
        async checkLoggedIn() {
            const response = await axios.get('/auth/is_authenticated');
            this.loggedIn = response.data.isAuthenticated;
        }
    },
    mounted() {
        this.checkLoggedIn();
    }
};
</script>

<template>
    <div class="surface-0 flex justify-content-center">
        <div id="home" class="landing-wrapper overflow-hidden">
            <div class="py-4 px-4 mx-0 md:mx-6 lg:mx-8 lg:px-8 flex align-items-center justify-content-between relative lg:static mb-3">
                <a class="flex align-items-center" href="#">
                    <img :src="logoUrl" alt="esun" height="50" class="mr-0 lg:mr-2" />&nbsp;&nbsp;&nbsp;
                    <div style="width: 300px"><span class="text-900 font-medium text-4xl line-height-3 mr-8" style="width: 250px">智能OCR服務</span> {{ version }} <span> </span></div>
                </a>
                <a class="cursor-pointer block lg:hidden text-700 p-ripple" v-ripple v-styleclass="{ selector: '@next', enterClass: 'hidden', leaveToClass: 'hidden', hideOnOutsideClick: true }">
                    <i class="pi pi-bars text-4xl"></i>
                </a>
                <div class="align-items-center surface-0 flex-grow-1 justify-content-between hidden lg:flex absolute lg:static w-full left-0 px-6 lg:px-0 z-2" style="top: 120px">
                    <ul class="list-none p-0 m-0 flex lg:align-items-center select-none flex-column lg:flex-row cursor-pointer"></ul>
                    <div class="flex justify-content-between lg:block border-top-1 lg:border-top-none surface-border py-3 lg:py-0 mt-3 lg:mt-0">
                        <Button label="Login" class="p-button-text p-button-rounded border-none font-light line-height-2 text-xl text-blue-500" @click="goLogin" v-if="!loggedIn"></Button>
                        <Button label="Register" class="p-button-rounded border-none ml-5 font-light text-white line-height-2 text-xl bg-blue-500" v-if="!loggedIn"></Button>
                    </div>
                </div>
            </div>

            <div
                id="hero"
                class="grid grid-nogutter surface-section text-800"
                style="background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), radial-gradient(77.36% 256.97% at 77.36% 57.52%, #eeefaf 0%, #c3e3fa 100%); clip-path: ellipse(150% 87% at 93% 13%)"
            >
                <div class="col-12 md:col-6 p-6 text-center md:text-left flex align-items-center">
                    <section>
                        <span class="block text-6xl font-bold mb-1">智能OCR服務</span>
                        <div class="text-6xl text-primary font-bold mb-3">Esun.OCR</div>
                        <p class="mt-0 mb-4 text-3xl text-700 line-height-3">由智金處電腦視覺專家研發設計，提供各式文/證件的影像辨識服務</p>
                    </section>
                </div>
                <div class="col-12 md:col-6 overflow-hidden my-image">
                    <img src="@/assets/img/hero-img.png" alt="Image" class="md:ml-auto block md:h-full animated" style="clip-path: polygon(8% 0, 100% 0%, 100% 100%, 0 100%)" />
                </div>
            </div>

            <div id="features" class="py-4 px-4 lg:px-8 mt-5 mx-0 lg:mx-8">
                <div class="grid justify-content-center">
                    <div class="col-12 text-center mt-8 mb-4">
                        <h2 class="text-900 font-normal mb-2">核心功能</h2>
                        <span class="text-600 text-2xl">這是一款致力於解決行內通用光學字元辨識的問題。</span>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('general')" @mouseleave="leave('general')" @click="goToPage('/features/ocr/general')">
                        <div
                            style="
                                height: 160px;
                                width: 750px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2));
                            "
                        >
                            <div v-if="isHovered['general']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">全文辨識</h5>
                                <span class="text-600">將影像中所有文字內容以及標註位置提取出來</span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-yellow-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-users text-2xl text-yellow-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">全文辨識</h5>
                                <span class="text-600">Intelligent OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('template')" @mouseleave="leave('template')" @click="goToPage('features/general/model-list')">
                        <div
                            style="
                                height: 160px;
                                width: 750px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['template']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">模板辨識</h5>
                                <span class="text-600">透過建立模板，可辨識影像中的特定要項。適用於固定樣式或格式的圖片及表單</span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-cyan-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-palette text-2xl text-cyan-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">模板辨識</h5>
                                <span class="text-600">Template OCR</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="features" class="py-4 px-4 lg:px-8 mt-5 mx-0 lg:mx-8">
                <div class="grid justify-content-center">
                    <div class="col-12 text-center mt-8 mb-4">
                        <h2 class="text-900 font-normal mb-2">人證辨識</h2>
                        <span class="text-600 text-2xl">已預設常見模板，提供身分證正反面、駕照、健保卡等影像進行OCR辨識以提取要項內容</span>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('id')" @mouseleave="leave('id')" @click="goToPage('features/ocr/id')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(145, 210, 204, 0.2));
                            "
                        >
                            <div v-if="isHovered['id']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">身份證辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-bluegray-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-bluegray-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">身份證辨識</h5>
                                <span class="text-600">ID OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('health')" @mouseleave="leave('health')" @click="goToPage('features/ocr/health_insurance')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['health']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">健保卡辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-orange-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-orange-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">健保卡辨識</h5>
                                <span class="text-600">Health Insurance Card OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('driver')" @mouseleave="leave('driver')" @click="goToPage('features/ocr/driver_license')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['driver']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">駕照辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-cyan-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-cyan-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">駕照辨識</h5>
                                <span class="text-600">Driver's License OCR</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="features" class="py-4 px-4 lg:px-8 mt-5 mx-0 lg:mx-8">
                <div class="grid justify-content-center">
                    <div class="col-12 text-center mt-8 mb-4">
                        <h2 class="text-900 font-normal mb-2">財證辨識</h2>
                        <span class="text-600 text-2xl">已預設常見模板，提供所得清單、扣繳憑單、存摺等影像進行OCR辨識以提取要項內容</span>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('fs')" @mouseleave="leave('fs')" @click="goToPage('features/ocr/financial_statement')">
                        <div
                            style="
                                height: 160px;
                                width: 750px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(145, 210, 204, 0.2));
                            "
                        >
                            <div v-if="isHovered['fs']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">所得清單辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-bluegray-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-bluegray-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">所得清單辨識</h5>
                                <span class="text-600">Financial Statement OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('ws')" @mouseleave="leave('ws')" @click="goToPage('features/ocr/withholding')">
                        <div
                            style="
                                height: 160px;
                                width: 750px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['ws']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">扣繳憑單辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-orange-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-orange-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">扣繳憑單辨識</h5>
                                <span class="text-600">Withholding OCR</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="features" class="py-4 px-4 lg:px-8 mt-5 mx-0 lg:mx-8">
                <div class="grid justify-content-center">
                    <div class="col-12 text-center mt-8 mb-4">
                        <h2 class="text-900 font-normal mb-2">票據辨識</h2>
                        <span class="text-600 text-2xl">已預設常見模板，提供提回支票正面、提回支票背面、匯款單影像進行OCR辨識以提取要項內容</span>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('remittance')" @mouseleave="leave('remittance')" @click="goToPage('features/ocr/remittance')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(145, 210, 204, 0.2));
                            "
                        >
                            <div v-if="isHovered['remittance']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">匯款單辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-bluegray-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-bluegray-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">匯款單辨識</h5>
                                <span class="text-600">Remittance OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('check_front')" @mouseleave="leave('check_front')" @click="goToPage('features/ocr/check_front')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['check_front']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">支票正面辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-orange-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-orange-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">支票正面辨識</h5>
                                <span class="text-600">Check Front OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-4 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0" @mouseover="over('check_back')" @mouseleave="leave('check_back')" @click="goToPage('features/ocr/check_back')">
                        <div
                            style="
                                height: 160px;
                                width: 500px;
                                padding: 2px;
                                border-radius: 10px;
                                background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2));
                            "
                        >
                            <div v-if="isHovered['check_back']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h5 class="mb-2 text-900">支票背面辨識</h5>
                                <span class="text-600"></span>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-cyan-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-cyan-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">支票背面辨識</h5>
                                <span class="text-600">Check Back OCR</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="py-4 px-4 mx-0 mt-8 lg:mx-8">
                <div class="grid justify-content-between"></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* #hero {
    background: linear-gradient(0deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.2)), radial-gradient(77.36% 256.97% at 77.36% 57.52%, #eeefaf 0%, #c3e3fa 100%);
    height: 700px;
    overflow: hidden;
}
#hero .animated {
    animation: up-down 2s ease-in-out infinite alternate-reverse both;
}
#faq .faq-list {
    padding: 0 100px;
}

#faq .faq-list ul {
    padding: 0;
    list-style: none;
}

#faq .faq-list li + li {
    margin-top: 15px;
}

#faq .faq-list li {
    padding: 20px;
    background: #fff;
    border-radius: 4px;
    position: relative;
}

#faq .faq-list a {
    display: block;
    position: relative;
    font-family: 'Poppins', sans-serif;
    font-size: 26px;
    line-height: 24px;
    font-weight: 500;
    padding: 0 30px;
    outline: none;
    cursor: pointer;
}

#faq .faq-list .icon-help {
    font-size: 30px;
    position: absolute;
    right: 0;
    left: 20px;
    color: #47b2e4;
}

#faq .faq-list .icon-show,
#faq .faq-list .icon-close {
    font-size: 24px;
    position: absolute;
    right: 0;
    top: 0;
}

#faq .faq-list p {
    margin-bottom: 0;
    padding: 10px 0 0 0;
}

#faq .faq-list .icon-show {
    display: none;
}

#faq .faq-list a.collapsed {
    color: #37517e;
    transition: 0.3s;
}

#faq .faq-list a.collapsed:hover {
    color: #47b2e4;
}

#faq .faq-list a.collapsed .icon-show {
    display: inline-block;
}

#faq .faq-list a.collapsed .icon-close {
    display: none;
}

@media screen and (min-width: 768px) {
    #hero {
        -webkit-clip-path: ellipse(150% 87% at 93% 13%);
        clip-path: ellipse(150% 87% at 93% 13%);
        height: 600px;
    }
}

@media screen and (min-width: 1300px) {
    #hero > img {
        position: absolute;
    }

    #hero > div > p {
        max-width: 550px;
    }
}

@media screen and (max-width: 1300px) {
    #hero {
        height: 700px;
    }

    #hero > img {
        position: static;
        transform: scale(1);
        margin-left: auto;
    }

    #hero > div > p {
        width: 100%;
        max-width: 100%;
    }
} */
</style>
