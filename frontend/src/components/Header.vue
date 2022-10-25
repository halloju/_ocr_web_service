<!-- <script setup>

</script> -->

<template>
  <header>
    <div class="container">
     <div class="row">
    <img
      alt=""
      class="num-1"
      src="https://static.overlay-tech.com/assets/a29acb82-a927-42fa-ba0a-59c8194dc5bb.svg"
    />
    <p class="esun-ocr">Esun. OCR</p>
    <div class="frame-1376">
      <div class="dashboard-black-24dp-1-1">
        <img
          alt=""
          class="vector"
          src="https://static.overlay-tech.com/assets/0c80f190-377f-45a2-a5ce-e120498cbfad.svg"
        />
      </div>
      <p class="nav-content">通用文件識別功能</p>
    </div>
    <div class="relative-wrapper-two">
      <div class="np-tag-888732-000000-1"></div>
      <div class="frame-1377">
        <img
          alt=""
          class="vector-two"
          src="https://static.overlay-tech.com/assets/57ef4a3c-d5fc-4a5f-888d-01e66bce4afb.svg"
        />
        <p class="nav-content">自定義模板</p>
      </div>
    </div>
    <div class="frame-1374">
      <div class="np-tag-888732-000000-2">
        <img
          alt=""
          class="vector"
          src="https://static.overlay-tech.com/assets/687cd02f-3a17-4439-8274-a745fff98f94.svg"
        />
      </div>
      <p class="nav-content">特殊文件識別功能</p>
    </div>
    <div class="user-info">
      <div class="group-137">
        <div class="ghost-two">
          <div class="ghost">
            <div class="vector-three"></div>
            <div class="vector-three"></div>
          </div>
        </div>
      </div>
      <div class="relative-wrapper-one">
        <p class="esb22005">ESB22005</p>
        <p class="admin-account">Admin account</p>
      </div>
    </div>
    </div>
  </div>
  </header>
</template>

<style lang="scss" scoped>
@import '../assets/css/_header.css';

// Colors
$black: rgba(0, 0, 0, 1);
$dark-cyan: rgba(7, 124, 149, 1);
$dark-gray: rgba(174, 174, 174, 1);
$sandy-brown: rgba(255, 193, 69, 1);
$transparent-black: rgba(0, 0, 0, 0.25);
$white: rgba(255, 255, 255, 1);

// Typographies
@mixin poppins-14-regular {
  font-family: "Poppins";
  font-size: 14px;
  font-weight: 400;
  line-height: normal;
}
.container {
  max-width: 100%;
  background-color: $dark-cyan;
  padding: 0 44.76px 0 28px;
  box-shadow: 0 4px 4px 0 $transparent-black;
  display: flex;
  justify-content: space-around;
  align-items: flex-start;
}
.num-1 {
  width: 80px;
  height: 34px;
  margin-top: 19px;
  margin-right: 16px;
}
.esun-ocr {
  max-width: 103px;
  font-family: "Poppins";
  font-size: 20px;
  font-weight: 700;
  line-height: normal;
  color: $white;
  margin-top: 20px;
  margin-right: 28px;
}
.frame-1376 {
  padding: 18px 37.65px 18px 37px;
  display: flex;
  align-items: flex-start;
}
.dashboard-black-24dp-1-1 {
  margin-right: 14.35px;
  padding: 4.13px 4.13px 4.12px 4.12px;
  display: flex;
  align-items: center;
}
.vector {
  flex: 1;
  align-self: stretch;
  object-fit: cover;
}
.nav-content {
  max-width: 160px;
  font-family: "Poppins";
  font-size: 20px;
  font-weight: 600;
  line-height: normal;
  color: $white;
  text-align: center;
  margin-top: 3px;
}
.relative-wrapper-two {
  position: relative;
}
.np-tag-888732-000000-1 {
  width: 42px;
  height: 42px;
  position: absolute;
  right: 7px;
  bottom: 11px;
}
.frame-1377 {
  padding: 21px 50px 20px 51px;
  display: flex;
  align-items: center;
  position: relative;
}
.vector-two {
  width: 14.92%;
  height: 96.43%;
  margin-right: 16px;
}
.nav-content {
  height: 28px;
  width: 138px;
  font-family: "Poppins";
  font-size: 20px;
  font-weight: 600;
  line-height: normal;
  color: $white;
  display: flex;
  align-items: center;
  text-align: center;
}
.frame-1374 {
  margin-right: 141px;
  padding: 14px 21px 13px 22px;
  display: flex;
  align-items: center;
}
.np-tag-888732-000000-2 {
  margin-right: 8px;
  padding: 7.88px 7.88px 7px 7px;
  display: flex;
  align-items: center;
}
.nav-content {
  height: 28px;
  width: 189px;
  font-family: "Poppins";
  font-size: 20px;
  font-weight: 600;
  line-height: normal;
  color: $white;
  display: flex;
  align-items: center;
  text-align: center;
}
.user-info {
  margin-top: 15px;
  display: flex;
  align-items: flex-start;
}
.group-137 {
  background-color: $sandy-brown;
  margin-right: 9.18px;
  border-radius: 50%;
  padding: 5px 6.06px 7.06px 6px;
  display: flex;
  align-items: flex-start;
}
.ghost-two {
  padding: 2.88px 3.6px 3.59px 3.59px;
  display: flex;
  align-items: center;
}
.ghost {
  background-size: 100% 100%;
  background-position: center;
  background-image: url("https://static.overlay-tech.com/assets/cbffd0be-e5e1-4257-9b0c-93d9640e17bd.svg");
  padding: 6.83px 4.67px 8.26px;
  display: flex;
  align-items: center;
}
.vector-three {
  width: 22.26%;
  height: 100%;
  background-color: $black;
  border-radius: 50%;
  &:not(:last-of-type) {
    margin-right: 3.59px;
  }
}
.relative-wrapper-one {
  margin-top: 17.53px;
  position: relative;
}
.esb22005 {
  max-width: 69px;
  font-family: "Poppins";
  font-size: 14px;
  font-weight: 600;
  line-height: normal;
  color: $white;
  position: absolute;
  left: 0;
  top: -17px;
}
.admin-account {
  max-width: 108px;
  color: $dark-gray;
  position: relative;
  @include poppins-14-regular;
}
</style>
