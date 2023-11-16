<script >
import {  ref, watch, reactive } from 'vue';
import Carousel from '@/components/Carousel.vue';
import img1 from '@/assets/img/template_step/step1.png';
import img2 from '@/assets/img/template_step/step2.png';
import img3_1 from '@/assets/img/template_step/step3-1.png';
import img3_2 from '@/assets/img/template_step/step3-2.png';
import img4 from '@/assets/img/template_step/step4.png';
import img5 from '@/assets/img/template_step/step5.png';
export default {
  name: 'TemplateCarousel',
  components: {
        Carousel
    },
  props: {
    show :{
      type: Boolean
    }
  },
  setup(props) {
    const dialogVisible = ref(props.show);

    watch(() => props.show, (newShowValue) => {
      dialogVisible.value = newShowValue;
    });
    const contentList = reactive([
        { key: 1, title: 'Step1. 圖檔上傳', content: 
        `
        <img src="${img1}" class="pop-img"/>
        <p class="pop-header">Step1. 圖檔上傳</p>
        <div class="text-container">
          <ol class="num-instructions">
              <li>命名「模板名稱」</li>
              <li>點選「新增圖片」或「+」按鈕，選取您欲建立的模版圖片</strong></li>
          </ol>
          <p class="text-title">注意事項:</p>
          <ul class="instructions">
              <li>請上傳<span class="red-text">空白的</span>表格或申請書圖檔 (例:未填寫的電子函證授權書、未填寫的XXX)</li>
              <li>若<span class="red-text">無空白的</span>表格或申請書圖檔善用<strong class="bold-text">Step4.遮罩標註</strong></li>
              <li>用來建立模板的圖片請勿包含個人機敏資訊及本行營業秘密，請參閱「IC-030_玉山銀行員工資訊安全作業要點」第六條（十）之即時通訊軟體使用規範</li>
          </ul>
        </div>
        `
         },
        { key: 2, title: 'Step2. 文字標註', content: `
        <img src="${img2}" class="pop-img" />
        <p class="pop-header">Step2. 文字標註</p>
        <div class="text-container">
          <ol class="num-instructions">
              <li>點選「新增標註」</li>
              <li>框選欲辨識的<strong>文字填寫範圍</strong>->輸入「欄位名稱」->選擇「區塊包含的字符」。(若有勾選框或簽名/印鑑欄位，請於下一步方塊標註時新增)</li>
          </ol>
          <p class="text-title">注意事項:</p>
          <ul class="instructions">
              <li>框選文字填寫範圍<span class="red-text">不含欄位名稱、表格框線或底線</span></li>
              <li>框選<span class="red-text">純文字</span>辨識範圍<span class="red-text">不含勾選框、原留印鑑框</span></li>
          </ul>
        </div>
        ` },
        { key: 3, title: 'Step3. 方塊標註', content: `
        <img src="${img3_1}" class="pop-img" />
        <p class="pop-header">Step3. 方塊標註</p>
        <div class="text-container">
          <ol class="num-instructions">
              <li>點選「新增標註」</li>
              <li>框選欲辨識的勾選框、原留印鑑(簽名) -> 輸入「欄位名稱」-> 選擇「區塊包含的字符」。</li>
          </ol>
          <p class="text-detail">※ 勾選框：辨識勾選、塗黑等方塊</p>
          <p class="text-detail">※ 原留印鑑框：辨識顧客是否有簽名或留存印鑑</p>
          <p class="text-title">注意事項:</p>
          <ul class="instructions">
              <li>只框選方框處，<span class="red-text">不含欄位名稱、選項文字</span>\n例：確認顧客勾選項目為何，只需框選方框處，<span class="red-text">不含</span>選項文字「新申請」、「變更」、「取消」。</li>
          </ul>
          <img src="${img3_2}" height="30" style="margin:10px 0px 0px 20px" />
        </div>
        
        ` },
        { key: 4, title: 'Step4. 遮罩標註', content: `
        <img src="${img4}" class="pop-img" />
        <p class="pop-header">Step4. 遮罩標註</p>
        <div class="text-container">
          <ol class="num-instructions">
              <li>點選「新增標註」</li>
              <li>框選表格、申請書或文件圖檔上的填寫區域與所有會變動的內容/你希望變成空白的內容。</li>
          </ol>
          <p class="text-title">注意事項:</p>
          <ul class="instructions">
              <li>例1: 以玉山名片為例, 遮罩標註會變動的內容與區域(部處、職稱、姓名等資訊)，僅留上半部進行模版比對。</li>
              <li>例2: 以香港傳真交易申請書為例，若缺乏空白模板，須將表單欄位的填寫內容遮罩，使表單像未填寫過的空白表單 (類似立可帶的功用！)</li>
          </ul>
        </div>
        ` },
        { key: 5, title: 'Step5. 模板確認', content: `
        <img src="${img5}" class="pop-img" />
        <p class="pop-header">Step5. 模板確認</p>
        <div class="text-container">
          <p>確認<strong>文字標註、方塊標註、遮罩標註</strong>皆無誤即可送出新增模板</p>
        </div>
        ` },
    ]);
    return {
        contentList,
        dialogVisible
    };
  }
};
</script>

<template>
  <Carousel :show="dialogVisible" :contentList="contentList"/>
</template>
<style>

.num-instructions > li {
    margin-left: 20px;
    display:list-item;
    list-style-type: decimal;
    font-weight: bold;
}
.instructions > li {
    margin-left: 20px;
    display:list-item;
    list-style-type: disc;
}
.red-text {
  color: red; /* This will make the text red */
}

.bold-text {
  font-weight: bold; /* This will make the text bold */
}

.text-container {
    flex: 1;
    text-align: left;
    padding-left: 10px;
    margin-bottom: 3px;
}

.image-container {
    display: flex;
    justify-content: space-between;
}

.pop-header {
	font-size: 20px;
	font-weight: bold;
	color: #3c4c5e;
	text-align: center;
  margin-bottom: 0.5rem;
}

.pop-img {
  height: 220px;
  margin-bottom: 1rem;
}
.text-title {
  margin: 0.5rem auto 0rem;
}
.text-detail {
  margin-top: 0.3rem;
  margin-bottom: 0rem;
  font-size: 14px;
}

</style>
