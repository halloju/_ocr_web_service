<template>
    <div class="sidebar">
        <div class="sidebarImg">
            <img :src="img_src"/>
        </div> 
        <div class="title">
            {{model}}
        </div>
        <div class="menu-items">
            <router-link :to="item.path" active-class="active" tag="button" exact class="side-btn" v-for="(item, i) in model_bar">
                <div class="link-container">
                    <p>{{item.title}}</p>
                </div>
                <div class="sub-container">
                    <p>{{item.sub_title}}</p>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'sidebar',
    props: {
        model: {
            type: String
        },
        img_src: {
            type: String
        },
        model_bar: {
            type: Object
        },
    },
    data() {
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
    font-size: 1.8rem;
    margin-top: 3vh;
    text-align: center;
}
.menu-items {
    display: flex;
    flex-direction: column;
    margin-top: 5vh;
}
.menu-items .link-container p {
    color: white;
}
.menu-items .sub-container {
    display:none;
}
.side-btn {
    text-align: left;
    border: none;
    height: 100px;
    width: 20vw;
    padding: 2.3vh 5vw;
    cursor: pointer;
    font-size: 24px;
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
@media (min-width: 2000px) {
.side-btn {
    text-align: left;
    border: none;
    height: 100px;
    width: 17vw;
    padding: 1.5vh 5vw;
    cursor: pointer;
    font-size: 25px;
    font-weight: 500;
    color: white;
    background-color: transparent;
    z-index: 100;
    }
}
@media (max-width: 1480px) {
.side-btn {
    text-align: left;
    border: none;
    height: 100px;
    width: 23vw;
    padding: 20px 70px;
    cursor: pointer;
    font-size: 21px;
    font-weight: 500;
    color: white;
    background-color: transparent;
    z-index: 100;
    }
}
@media (max-width: 1060px) {
.title {
    color: white;
    font-size: 1.2rem;
    margin-top: 3vh;
    text-align: center;
}
.side-btn {
    text-align: left;
    border: none;
    height: 100px;
    width: 20vw;
    padding: 2vh 6vw;
    cursor: pointer;
    font-size: 21px;
    font-weight: 500;
    color: white;
    background-color: transparent;
    z-index: 100;
    }
.side-btn .link-container p {
    display: none;
}
.menu-items .sub-container {
    display: block;
}
.menu-items .sub-container p {
    color: white;
}
}
</style>