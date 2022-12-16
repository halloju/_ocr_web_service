<script>
import Card from '@/components/Card.vue';

export default {
    name: 'BoxCard',
    mounted() {
        this.recs = this.$store.state[this.Boxes[0].name];
    },
    components: {
        Card
    },
    computed: {
        recs() {
            return this.$store.state[this.Boxes[0].name];
        }
    },
    props: {
        Boxes: {
            type: Array,
            required: false
        }
    }
};
</script>

<template>
    {{recs}}
    <div v-for="box in this.Boxes" class="surface-section" style="width: 400px">
        <div class="font-medium text-3xl text-900 mb-3">{{ box.title }}</div>
        <ul class="list-none p-0 m-0">
            <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 w-6 md:w-2 font-medium">No.</div>
                <div class="text-900 w-full md:w-4 md:flex-order-0 flex-order-1">要項名稱</div>
                <div class="text-900 w-6 md:w-3 flex justify-content-center">操作</div>
            </li>
        </ul>
        <Card :key="box.name" :boxName="box.name" :boxTitle="box.name" />
    </div>
</template>
