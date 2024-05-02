<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';

export default defineComponent({
    name: 'BrowseModeComponent',
    props: {
        formData: {
            type: Array
        }
    },
    data() {
        return {
            mergedText: ''
        };
    },
    methods: {
        copyAllResults() {
            navigator.clipboard
                .writeText(this.mergedText)
                .then(() => {
                    ElMessage({
                        message: '複製成功',
                        type: 'info'
                    });
                })
                .catch((err) => {
                    console.log(err);
                    ElMessage({
                        message: '複製失敗',
                        type: 'warning'
                    });
                });
        }
    },
    created() {
        this.mergedText = this.formData.map((item) => item.annotation.text).join(' ');
        console.log('browse-mode-component mergedText:', this.mergedText);
    },
    watch: {
        formData(newValue) {
            this.mergedText = newValue.map((item) => item.annotation.text).join(' ');
            console.log('browse-mode-component received formData:', newValue);
        }
    },
    mounted() {
        // this.mergedText = this.formData.map((item) => item.annotation.text).join(' ');
        console.log('browse-mode-component mergedText mounted:', this.mergedText);
    }
});
</script>

<template>
    <div class="container">
        <div class="header">
            <!-- This div will hold the button and ensure it's placed on the right -->
            <button class="uiStyle sizeS btnGreen" @click="copyAllResults">複製</button>
        </div>
        <el-input type="textarea" :rows="10" readonly :value="mergedText"></el-input>
    </div>
</template>

<style>
.container {
    /* Flex column will stack children vertically */
    display: flex;
    flex-direction: column;
}

.header {
    /* Align the button to the right */
    display: flex;
    justify-content: flex-end;
    margin-bottom: 8px; /* Adjust space between button and input as needed */
}
</style>
