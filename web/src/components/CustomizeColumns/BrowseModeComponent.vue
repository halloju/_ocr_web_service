<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BrowseModeComponent',
    props: {
    },
    methods: {
        copyAllResults(result) {
            // Copy the individual result to the clipboard
            navigator.clipboard.writeText(result);
        }
    }
});
</script>

<template>
    <el-table-column>
        <template v-slot:header>
            <span>辨識結果</span>
            <el-button type="text" @click="copyAllResults">Copy All</el-button>
        </template>
        <template v-slot="scope">
            <div>
                <span>{{ scope.row.combinedResult }}</span>
            </div>
        </template>
    </el-table-column>
</template>
