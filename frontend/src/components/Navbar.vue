<template>
  <div class="page-wrapper">
    <div class="nav-wrapper">
      <nav class="menu">
        <!-- <div class="navbar-toggle">
          <i class="fa fas fa-bars"></i>
         </div> -->
        <a href="#" class="logo">
          <img src="https://static.overlay-tech.com/assets/a29acb82-a927-42fa-ba0a-59c8194dc5bb.svg" alt="logo">
          <span>Esun.OCR</span>
        </a>
        <ul class="navbar">
          <li class="navbar-links">
              <img src="https://static.overlay-tech.com/assets/0c80f190-377f-45a2-a5ce-e120498cbfad.svg"/>
              <p>通用文件識別功能</p>
          </li>
          <li class="navbar-links">
            <img src="https://static.overlay-tech.com/assets/57ef4a3c-d5fc-4a5f-888d-01e66bce4afb.svg"/>
            <p>自定義模板</p>
          </li>
          <li class="navbar-links">
            <img src="https://static.overlay-tech.com/assets/687cd02f-3a17-4439-8274-a745fff98f94.svg"/>
            <p>特殊文件識別功能</p>
          </li>
        </ul>
        <div class="user">
          <div class="group-circle">
            <div class="user-icon"></div>
          </div>
          <div class="relative-wrapper-one">
            <p class="esb">ESB22005</p>
            <p class="admin-account">Admin account</p>
          </div>
        </div>
        <div class="navbar-toggle">
            <i class="fa fas fa-bars"></i>
        </div>
      </nav>
    </div>
  </div>   
</template>
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, Helvetica, sans-serif;
}
.menu {
  display: flex;
  background-color: #008b8b;
  height: 48px;
  width: 100%;
  align-items: center;
  justify-content: flex;
  padding: 2px;
}
.logo {
  display: flex;
  align-items: center;
  width: 220px;
  margin-left: 10px;
  margin-right: 10px;
}
.logo span {
  margin-left: 15px;
  color: white;
  font-weight: bold;
  font-size: 1.7rem;
}
.navbar {
  display: flex;
  flex: auto;
  justify-content: flex-end;
}
.navbar li {
  display: flex;
  font-weight: bold;
  font-size: 1.2rem;
  margin-left: 25px;
  margin-right: 25px;
}
.navbar li img{
  max-width: 27px;
}
.navbar li p {
  color: white;
  margin-left: 10px;
}
.navbar-links:hover {
  background-color: #578F8D;
}
.navbar-user:hover {
  background-color: #578F8D;
}
.user {
  width: 200px;
  display: flex;
  align-items: center;
}
.group-circle {
  background-color: #FFC145;
  margin-right: 10px;
  border-radius: 50%;
  padding: 3px 3px 3px 3px;
  display: flex;
  align-items: center;
  width: 30px;
  height: 30px;
}
.user-icon {
  background-size: 100% 100%;
  background-position: center;
  background-image: url("https://static.overlay-tech.com/assets/cbffd0be-e5e1-4257-9b0c-93d9640e17bd.svg");
  padding: 8px 11px;
  display: flex;
  justify-content: center;
}
.relative-wrapper-one p {
  color: white;
  font-weight: bold;
}
.navbar-toggle {
  display: none;
}
@media (max-width: 1130px) {
  .navbar {
    position: absolute;
    top: 48px;
    right: 0%;
    width: 270px;
    height: 30xvh;
    background-color: #008b8b;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    border-radius: 10px;
  }
  .navbar li {
    display: flex;
    margin: 30px 0;
    padding: 0px 25px;
  }
  .navbar-links {
    width: 100%;
    text-align: center;
  }
  .navbar-links:hover {
  background-color: #578F8D;
  }
  .fa {
    color: white;
  }
  .navbar-toggle {
    display: flex;
    font-size: 35px;
  }
  .user {
    width: 200px;
    display: flex;
    justify-content: center;
  }
}

</style>