<script>
export default {
    name: 'landing',
    data() {
        return {
            logoUrl: `../src/assets/img/esun-ocr-logo.svg`,
            version: import.meta.env.VITE_APP_VERSION,
            isHovered: {}
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
        }
    }
};

</script>

<template>
    <div class="surface-0 flex justify-content-center">
        <div id="home" class="landing-wrapper overflow-hidden">
            <div class="py-4 px-4 mx-0 md:mx-6 lg:mx-8 lg:px-8 flex align-items-center justify-content-between relative lg:static mb-3">
                <a class="flex align-items-center" href="#">
                    <img :src="logoUrl" alt="esun" height="50" class="mr-0 lg:mr-2" />&nbsp;&nbsp;&nbsp;<div style="width: 300px"><span class="text-900 font-medium text-4xl line-height-3 mr-8" style="width: 250px">智能OCR服務</span> {{version}} <span>  </span></div>
                </a>
                <a class="cursor-pointer block lg:hidden text-700 p-ripple" v-ripple v-styleclass="{ selector: '@next', enterClass: 'hidden', leaveToClass: 'hidden', hideOnOutsideClick: true }">
                    <i class="pi pi-bars text-4xl"></i>
                </a>
                <div class="align-items-center surface-0 flex-grow-1 justify-content-between hidden lg:flex absolute lg:static w-full left-0 px-6 lg:px-0 z-2" style="top: 120px">
                    <ul class="list-none p-0 m-0 flex lg:align-items-center select-none flex-column lg:flex-row cursor-pointer">
                        <li>
                            <a @click="smoothScroll('#hero')" class="flex m-0 md:ml-5 px-0 py-3 text-900 font-medium text-2xl line-height-3 p-ripple" v-ripple>
                                <span>首頁</span>
                            </a>
                        </li>
                        <li>
                            <a @click="smoothScroll('#features')" class="flex m-0 md:ml-5 px-0 py-3 text-900 font-medium text-2xl line-height-3 p-ripple" v-ripple>
                                <span>核心功能</span>
                            </a>
                        </li>
                        <li>
                            <a @click="smoothScroll('#highlights')" class="flex m-0 md:ml-5 px-0 py-3 text-900 font-medium text-2xl line-height-3 p-ripple" v-ripple>
                                <span>關於產品</span>
                            </a>
                        </li>
                        <li>
                            <a @click="smoothScroll('#faq')" class="flex m-0 md:ml-5 px-0 py-3 text-900 font-medium text-2xl line-height-3 p-ripple" v-ripple>
                                <span>常見問題</span>
                            </a>
                        </li>
                    </ul>
                    <div class="flex justify-content-between lg:block border-top-1 lg:border-top-none surface-border py-3 lg:py-0 mt-3 lg:mt-0">
                        <Button label="Login" class="p-button-text p-button-rounded border-none font-light line-height-2 text-xl text-blue-500" @click="goLogin"></Button>
                        <Button label="Register" class="p-button-rounded border-none ml-5 font-light text-white line-height-2 text-xl bg-blue-500"></Button>
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
                        <p class="mt-0 mb-4 text-3xl text-700 line-height-3">由智金處電腦視覺專家研發設計，解決行內 PDF、身份證、健保卡圖片辨識等問題。</p>

                        <Button label="Learn More" type="button" class="mr-3 p-button-raised" @click="goLogin"></Button>
                        <Button label="Live Demo" type="button" class="p-button-outlined"></Button>
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

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('general')"
                        @mouseleave="leave('general')"
                        @click="goToPage('/features/ocr/general')">
                        <div
                            style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(187, 199, 205, 0.2))"
                        >
                            <div v-if="isHovered['general']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h3 class="mb-2 text-900">全文辨識</h3>
                                <h5>將影像中所有文字內容以及標註位置提取出來</h5>
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

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('template')"
                        @mouseleave="leave('template')"
                        @click="goToPage('features/general/model-list')">
                        <div
                            style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(145, 226, 237, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(172, 180, 223, 0.2))"
                        >
                            <div v-if="isHovered['template']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h3 class="mb-2 text-900">模板辨識</h3>
                                <h5>透過建立模板，可辨識影像中的特定要項。適用於固定樣式或格式的圖片及表單</h5>
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


                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('id')"
                        @mouseleave="leave('id')"
                        @click="goToPage('features/ocr/id')">
                        <div
                            style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(251, 199, 145, 0.2)), linear-gradient(180deg, rgba(253, 228, 165, 0.2), rgba(145, 210, 204, 0.2))"
                        >   
                            <div v-if="isHovered['id']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h3 class="mb-2 text-900">人證辨識</h3>
                                <h5>已預設常見模板，提供身分證正反面、駕照、健保卡等影像進行OCR辨識以提取要項內容</h5>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-bluegray-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-id-card text-2xl text-bluegray-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">人證辨識</h5>
                                <span class="text-600">ID OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('financial')"
                        @mouseleave="leave('financial')"
                        @click="goToPage('features/ocr/financial_statement')">
                        <div
                            style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(246, 158, 188, 0.2)), linear-gradient(180deg, rgba(145, 226, 237, 0.2), rgba(160, 210, 250, 0.2))"
                        >   
                            <div v-if="isHovered['financial']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h3 class="mb-2 text-900">財證辨識</h3>
                                <h5>已預設常見模板，提供所得清單、扣繳憑單、存摺等影像進行OCR辨識以提取要項內容</h5>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-orange-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-star text-2xl text-orange-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">財證辨識</h5>
                                <span class="text-600">Financial Statement OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pr-5 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('bill')"
                        @mouseleave="leave('bill')"
                        @click="goToPage('features/ocr/remittance')">
                        <div
                            style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(187, 199, 205, 0.2), rgba(246, 158, 188, 0.2)), linear-gradient(180deg, rgba(145, 226, 237, 0.2), rgba(160, 210, 250, 0.2))"
                        >   
                            <div v-if="isHovered['bill']" class="p-3 surface-card h-full" style="border-radius: 8px">
                                <h3 class="mb-2 text-900">票據辨識</h3>
                                <h5>已預設常見模板，提供提回支票正面、提回支票背面、匯款單影像進行OCR辨識以提取要項內容</h5>
                            </div>
                            <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                                <div class="flex align-items-center justify-content-center bg-orange-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                    <i class="pi pi-fw pi-star text-2xl text-orange-700"></i>
                                </div>
                                <h5 class="mb-2 text-900">票據辨識</h5>
                                <span class="text-600">Bill OCR</span>
                            </div>
                        </div>
                    </div>

                    <div class="col-12 md:col-12 lg:col-6 p-0 lg:pb-5 mt-4 lg:mt-0"
                        @mouseover="over('bill2')"
                        @mouseleave="leave('bill2')">
                    <div
                        style="height: 160px; padding: 2px; border-radius: 10px; background: linear-gradient(90deg, rgba(251, 199, 145, 0.2), rgba(246, 158, 188, 0.2)), linear-gradient(180deg, rgba(172, 180, 223, 0.2), rgba(212, 162, 221, 0.2))"
                    >
                        <div v-if="isHovered['bill2']" class="p-3 surface-card h-full" style="border-radius: 8px">
                            <span></span>
                        </div>
                        <div v-else class="p-3 surface-card h-full" style="border-radius: 8px">
                            <div class="flex align-items-center justify-content-center bg-pink-200 mb-3" style="width: 3.5rem; height: 3.5rem; border-radius: 10px">
                                <i class="pi pi-fw pi-moon text-2xl text-pink-700"></i>
                            </div>
                            <h5 class="mb-2 text-900"></h5>
                            <span class="text-600"></span>
                        </div>
                    </div>
                </div>

                </div>
            </div>

            <div id="highlights" class="py-4 px-4 lg:px-8 mx-0 my-6 lg:mx-8">
                <div class="text-center">
                    <h2 class="text-900 font-normal mb-2">關於產品</h2>
                    <span class="text-600 text-2xl">齊心齊力打造更完善、優良的服務體驗</span>
                </div>

            </div>

            <!-- ======= Frequently Asked Questions Section ======= -->
            <div id="faq" class="faq section-bg">
                <div class="container" data-aos="fade-up">
                    <div class="text-center">
                        <h2 class="text-900 font-normal mb-2 text-5xl">常見問題</h2>
                    </div>

                    <div class="faq-list text-2xl">
                        <ul>
                            <li data-aos="fade-up" data-aos-delay="100">
                                <i class="bx bx-help-circle icon-help"></i>
                                <a data-bs-toggle="collapse" class="collapse" data-bs-target="#faq-list-1">這個需要付費嗎？<i class="bx bx-chevron-down icon-show"></i><i class="bx bx-chevron-up icon-close"></i></a>
                                <div id="faq-list-1" class="collapse show" data-bs-parent=".faq-list">
                                    <p>完全不用！請盡情享受</p>
                                </div>
                            </li>

                            <li data-aos="fade-up" data-aos-delay="400">
                                <i class="bx bx-help-circle icon-help"></i>
                                <a data-bs-toggle="collapse" data-bs-target="#faq-list-4" class="collapsed">這可以幹麼？ <i class="bx bx-chevron-down icon-show"></i><i class="bx bx-chevron-up icon-close"></i></a>
                                <div id="faq-list-4" class="collapse" data-bs-parent=".faq-list">
                                    <p>解決您的辨識問題！</p>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <!-- End Frequently Asked Questions Section -->

            <div class="py-4 px-4 mx-0 mt-8 lg:mx-8">
                <div class="grid justify-content-between">
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#hero {
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
}
</style>
