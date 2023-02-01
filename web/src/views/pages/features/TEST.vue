<script>
import Image from '@/assets/img/hero-img.png';
import Annotation from '@/components/Annotation.vue';

export default {
    components: {
        Annotation
    },
    data() {
        return {
            containerId: 'my-pic-annotation',
            containerId2: 'my-pic-annotation-output',
            editMode: true,
            language: 'en',
            imageSrc: Image,
            localStorageKey: 'storage',
            width: 1200,
            height: 600,
            dataCallback: '',
            initialData:
                '[{"type":"rect","name":"shape-1673851677198","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項一","text":"","linkTitle":"","link":""},"x":121.30823537700691,"y":186.11122465281173,"width": 200,"height":215.33333333333334},{"type":"rect","name":"shape-1673851944263","fill":"#b0c4de","opacity":0.5,"stroke":"#00f","draggable":true,"strokeWidth":2,"strokeScaleEnabled":false,"annotation":{"title":"要項二","text":"","linkTitle":"","link":""},"x":219.74836905871385,"y":37.62814538676607,"width":150.5125815470643,"height":150.5125815470643}]',
            initialDataId: null
        };
    },
    methods: {
        callback(data) {
            document.getElementById('output').innerHTML = data;
        }
    }
};
</script>

<template>
    <div>
        <p>Edit:</p>
        <Annotation :containerId="containerId" :editMode="true" :imageSrc="imageSrc" :localStorageKey="localStorageKey" :width="width" :height="height" :dataCallback="callback" initialData="" :initialDataId="initialDataId"></Annotation>

        <p>Data:</p>
        <div>
            <textarea id="output" style="width: 80%; height: 200px"></textarea>
        </div>
        <p>Show:</p>
        <Annotation containerId="my-pic-annotation-output" :editMode="false" :imageSrc="imageSrc" :width="width" :height="height" dataCallback="" :initialData="initialData" :initialDataId="initialDataId"></Annotation>
    </div>
</template>
