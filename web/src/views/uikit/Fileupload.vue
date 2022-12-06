<template #header="{ chooseCallback, uploadCallback, clearCallback, files }">
    <div class="flex flex-wrap justify-content-between align-items-center flex-1 gap-2">
        <div class="flex gap-2">
            <Button @click="chooseCallback()" icon="pi pi-images" class="p-button-rounded"></Button>
            <Button @click="uploadCallback()" icon="pi pi-cloud-upload" class="p-button-rounded p-button-success" :disabled="!files || files.length === 0"></Button>
            <Button @click="clearCallback()" icon="pi pi-times" class="p-button-rounded p-button-danger" :disabled="!files || files.length === 0"></Button>
        </div>
        <ProgressBar :value="totalSizePercent" :showValue="false" :class="['md:w-20rem h-1rem w-full md:ml-auto', { 'exceeded-progress-bar': totalSizePercent > 100 }]"
            ><span class="white-space-nowrap">{{ totalSize }}B / 1Mb</span></ProgressBar
        >
    </div>
</template>
<template #content="{ files, uploadedFiles, onUploadedFileRemove, onFileRemove }">
    <div v-if="files.length > 0">
        <h5>Pending</h5>
        <div class="flex flex-wrap p-5 gap-5">
            <div v-for="(file, index) of files" :key="file.name + file.type + file.size" class="card m-0 px-6 flex flex-column border-1 surface-border align-items-center gap-3">
                <div>
                    <img role="presentation" :alt="file.name" :src="file.objectURL" height="50" class="shadow-2" />
                </div>
                <span class="font-semibold">{{ file.name }}</span>
                <div>{{ formatSize(file.size) }}</div>
                <Badge value="Pending" severity="warning" />
                <Button icon="pi pi-times" @click="onRemoveTemplatingFile(file, onFileRemove, index)" class="p-button-outlined p-button-danger p-button-rounded" />
            </div>
        </div>
    </div>

    <div v-if="uploadedFiles.length > 0">
        <h5>Completed</h5>
        <div class="flex flex-wrap p-0 sm:p-5 gap-5">
            <div v-for="(file, index) of uploadedFiles" :key="file.name + file.type + file.size" class="card m-0 px-6 flex flex-column border-1 surface-border align-items-center gap-3">
                <div>
                    <img role="presentation" :alt="file.name" :src="file.objectURL" width="100" class="shadow-2" />
                </div>
                <span class="font-semibold">{{ file.name }}</span>
                <div>{{ formatSize(file.size) }}</div>
                <Badge value="Completed" class="mt-3" severity="success" />
                <Button icon="pi pi-times" @click="onUploadedFileRemove(index)" class="p-button-outlined p-button-danger p-button-rounded" />
            </div>
        </div>
    </div>
</template>
<template #empty>
    <div class="flex align-items-center justify-content-center flex-column">
        <i class="pi pi-cloud-upload border-2 border-circle p-5 text-8xl text-400 border-400" />
        <p class="mt-4 mb-0">Drag and drop files to here to upload.</p>
    </div>
</template>
