<template>
    <div>
        <p>Edit:</p>
        <Annotation
            :containerId="containerId"
            :editMode="true"
            :language="language"
            :imageSrc="imageSrc"
            :localStorageKey="localStorageKey"
            :width="width"
            :height="height"
            :dataCallback="dataCallback"
            initialData=""
            :initialDataId="initialDataId"
        ></Annotation>


        <p>Data:</p>
        <div>
            <textarea id="output" style="width: 80%; height: 200px;"></textarea>
        </div>
        <p>Show:</p>
        <Annotation
            containerId="my-pic-annotation-output"
            :editMode="false"
            :language="language"
            :imageSrc="imageSrc"
            :width="width"
            :height="height"
            :dataCallback="dataCallback"
            :initialData="initialData"
            :initialDataId="initialDataId"
        ></Annotation>
    </div>
</template>
  
<script>
import Image from '@/assets/img/hero-img.png'
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
        editMode: 'en',
        imageSrc: Image,
        localStorageKey: "storage",
        width: 1200,
        height: 600,
        dataCallback: '',
        initialData: '',
        initialDataId: null,
    }
},
}

</script>

