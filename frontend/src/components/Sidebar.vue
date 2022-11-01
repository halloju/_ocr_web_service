<template>
    <div class="sidebar">
        <div class="sidebarImg">
            <img :src="img_src"/>
        </div> 
        <div class="title">
            {{model}}
        </div>
        <div class="menu-items">
            <router-link :to="item.path" active-class="active" tag="button" exact class="side-btn" v-for="(item, i) in model_bar[model]">
                <div class="link-container">
                    {{item.title}}
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
import feature2 from '@/assets/images/feature2.svg'
export default {
    name: 'sidebar',
    data() {
        return {
            model: "新增自定義模板",
            img_src: feature2,
            model_bar: {"新增自定義模板": [{title: "1. 範例圖檔上傳", path: "/define/step1"},
                                        {title: "2. 文字位置標註", path: "/define/step2"},
                                        {title: "3. 方塊位置標註", path: "/define/step3"},
                                        {title: "4. Mask 位置標註", path: "/define/step4"},
                                        {title: "5. 資訊確認", path: "/define/step5"},
                                        ]},
        }
    } 
}
</script>

<style scoped>
.sidebarImg{
    text-align: center;
}
.sidebarImg img{
    margin-top: 3vh;
    width: 30%;
}
.title {
    color: white;
    font-size: 24px;
    margin-top: 3vh;
    text-align: center;
}
.menu-items {
    display: flex;
    flex-direction: column;
    margin-top: 5vh;
}
.side-btn {
    border: none;
    height: 80px;
    max-width: 300px;
    padding: 10px 70px;
    cursor: pointer;
    font-size: 21px;
    font-weight: 500;
    color: white;
    background-color: transparent;
    z-index: 100;
}
.side-btn:focus {
    outline: none;
    color: white;
}
.side-btn .link-container {
    margin-top: 1vh;
    color: white;
    width: 300px;
}
.side-btn.active {
    position: relative;
    background-color: #09747A;
    color: #10A0A7;
    font-weight: bold;
    margin-left: 0.7vw;
    border-radius: 50px 0 0 50px;
    z-index: 0;
}
.side-btn.active::before {
    top: -30px;
    
}
.side-btn.active::after {
    bottom: -30px;
    
}
.side-btn.active::before, .side-btn.active::after {
    position: absolute;
    content: "";
    right: 0;
    height: 30px;
    width: 30px;
    background-color: #09747A;
    
}
.side-btn.active .link-container::before {
    top: -60px;
    
}
.side-btn.active .link-container::after {
    bottom: -60px;
    z-index: 99;
    
}
.side-btn.active .link-container::before, .side-btn.active .link-container::after {
    position: absolute;
    content: "";
    right: 0px;
    height: 60px;
    width: 60px;
    border-radius: 50%;
    background-color: #10A0A7;
    
}
</style>