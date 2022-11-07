<template>
    <div class="loginWrapper">
        <div class="card">
            <img src="@/assets/images/esun-ocr-logo.svg" class="home-logo"/>
            <h1>E.SUN OCR 服務</h1>
            <p class="card-title">使用者登入</p>
            <div class="account">
                <p class="feature-content">員工編號</p>
                <input placeholder="請輸入您的員工編號5碼" required pattern="[0-9]{5}">
            </div>
            <div class="pwd">
                <p class="feature-content">密碼</p>
                <input placeholder="請輸入您的密碼" type="password" required>
            </div>
            <div class="buttons">
                <button type="submit" class="login-button" id="submit" @click="login">登入</button>
            </div>
            <div class="others">
                <span class="not-register-link">尚未註冊?&nbsp;</span>
                <span class="register-link"><router-link to="./userinfo">註冊</router-link></span>
            </div>
        </div>
    </div>
</template>
  
<style scoped>
.loginWrapper {
    background: url('@/assets/images/dashborad-bg.svg') no-repeat;
    background-size: 130%;
    background-position: bottom;
    background-color: #09747A;
    border-radius: 0px;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.loginWrapper .card{
    background-color: white;
    height: 70vh;
    width: 30vw;
    max-width: 400px;
    border-radius: 2vw 2vw 2vw 2vw;
    text-align: center;
}
.card .home-logo{
    height: 10vh;
    margin-top: 6vh;
    text-align: center;
}
.card h1 {
    margin-top: 2vh;
    font-size: 2.5rem;
    font-weight: bold;
    color: #008b8b;
}
.card .card-title {
    margin-top: 2vh;
    font-size: 1.5rem;
    font-weight: bold;
}
.card .account {
    margin-top: 3%;
    margin-left: 12%;
    font-size: 1.3rem;
    font-weight: bold;
    text-align: left;
}
.card .pwd {
    margin-top: 3%;
    margin-left: 12%;
    font-size: 1.3rem;
    font-weight: bold;
    text-align: left;
}
.card input {
    margin-top: 20px;
    width: 22vw;
    height: 4vh;
    max-width: 300px;
    text-align: left;
}
.buttons {
    margin-top: 1vh;
    text-align: center;
}
.buttons .login-button{
    background-image: linear-gradient(155deg,#F79E0E, #EEBD23);
    padding: 10px 130px;
    border-radius: 1vw 1vw 1vw 1vw;
    color: white;
    font-size: 1.5rem;
    font-weight: bold;
    margin-top: 1vw;
    border: none;
}
.others {
    margin-top: 1.5vh;
    margin-left: 12%;
    text-align: left;
}
</style>
<script>
export default {
    name: 'Home',
    data() {
        return {

        };
    },
    methods: {
            login() {
                this.$router.push({name:"Home"})
            }
        }

    };
</script>