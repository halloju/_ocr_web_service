<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';

export default defineComponent({
    name: 'BrowseModeComponent',
    props: {
        formData: {
            type: Array,
            default: () => [] // Default to an empty array if no formData is passed
        }
    },
    data() {
        return {
            mergedText: '',
            localFormData: [],
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
        },
        concatTextResults(textList, filters) {
            if (textList.length < 2) return textList.join('');
            if (!filters.includes('tchinese')) {
                return textList.join(' ');
            } else {
                let textResults = textList[0];
                let previousText = textList[0];

                for (let i = 1; i < textList.length; i++) {
                    const text = textList[i];
                    if (previousText.charCodeAt(previousText.length - 1) >= 128 && text.charCodeAt(0) >= 128) {
                        textResults += text;
                    } else {
                        textResults += ` ${text}`;
                    }
                    previousText = text;
                }

                return textResults;
            }
        },
        getYCenter(point) {
            if (!point) {
                console.error('Invalid or incomplete point data:', point);
                return 0; // or handle this case appropriately
            }
            return point.y + point.height / 2;
        },
        getXCenter(point) {
            return point.x + point.width / 2;
        },
        groupLineResults(results, margin = 0.5) {
            if (results.length < 2) return results;
            const sortedResults = [];
            let tempResults = [];
            let previousYCenter = results[0].yCenter;

            results.forEach((result, index) => {
                const yCenter = result.yCenter;
                const charHeight = result.height;

                if (yCenter < previousYCenter - charHeight * margin || yCenter > previousYCenter + charHeight * margin) {
                    tempResults.sort((a, b) => a.xCenter - b.xCenter);
                    if (tempResults.length > 0) {
                        tempResults[tempResults.length - 1].text += '\n';
                    }
                    sortedResults.push(...tempResults);
                    tempResults = [];
                }

                tempResults.push(result);
                previousYCenter = yCenter;

                if (index === results.length - 1 && tempResults.length !== 0) {
                    tempResults.sort((a, b) => a.xCenter - b.xCenter);
                    sortedResults.push(...tempResults);
                }
            });

            return sortedResults;
        },
        sortOcrResults(results) {
            let augmentedResults = results.map((item) => ({
                ...item,
                yCenter: this.getYCenter(item),
                xCenter: this.getXCenter(item)
            }));
            const ySortedResults = augmentedResults.sort((a, b) => a.yCenter - b.yCenter);
            return this.groupLineResults(ySortedResults, 0.5);
        }
    },
    created() {
        this.localFormData = JSON.parse(JSON.stringify(this.formData));
    },
    watch: {
        formData: {
            handler(newValue) {
                this.localFormData = JSON.parse(JSON.stringify(newValue));
                const sortedOcrResults = this.sortOcrResults(this.localFormData);
                const textResults = this.concatTextResults(
                    sortedOcrResults.map((item) => item.annotation.text),
                    []
                );
                this.mergedText = textResults;
            },
            deep: true,
            immediate: true
        }
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
