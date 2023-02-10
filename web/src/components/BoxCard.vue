<script lang="ts">
import Card from '@/components/Card.vue';
import Icon from '@/components/Icon.vue';
import { mapState } from 'vuex';

export default {
    name: 'BoxCard',
    components: {
        Card,
        Icon
    },
    props: {
        Boxes: {
            type: Array,
            required: false
        }
    },
    data() {
        return {
            isShapesVisible: {
                text: true,
                box: true,
                mask: true
            }
        };
    },
    methods: {
        toggleShowShapes(name) {
            this.isShapesVisible[name] = !this.isShapesVisible[name];
            this.$emit('toggleShowShapes', name, this.isShapesVisible[name]);
        }
    },
    computed: {
        ...mapState(['selfDefinedRecs']),
        recs() {
            return this.selfDefinedRecs[this.Boxes[0].name] || [];
        },
        canEdit() {
            return this.Boxes.length <= 1;
        }
    }
};
</script>

<template>
    {{ recs }}
    <div v-for="box in this.Boxes" :key="box.name" class="surface-section" style="width: 400px">
        <div class="font-medium text-3xl text-900 mb-3">
            {{ box.title }}
            <a href="#" @click.prevent="toggleShowShapes(box.name)" :title="this.isShapesVisible[box.name] ? 'show_shapes' : 'hide_shapes'"><icon :type="this.isShapesVisible[box.name] ? 'shapes-on' : 'shapes-off'" /></a>
        </div>
        <ul class="list-none p-0 m-0">
            <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 w-6 md:w-2 font-medium">No.</div>
                <div class="text-900 w-full md:w-4 md:flex-order-0 flex-order-1">要項名稱</div>
                <div class="text-900 w-6 md:w-3 flex justify-content-center">操作</div>
            </li>
        </ul>
        <Card :key="box.name" :boxName="box.name" :boxTitle="box.name" :canEdit="this.canEdit" />
    </div>
</template>
