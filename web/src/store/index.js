import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        // 自定義模板
        // selfDefinedRecs: { text: [], box: [], mask: [], name: [], id: [] },
        // 通用辨識
        general_boxes: [],
        general_upload_image: [],
        general_upload_res: [],
        // 模板辨識
        template_id: '',
        createNew: false,
        templateName: '',
    },

    mutations: {
        GENERAL_IMAGE_OCR_RESULTS_UPDATE(state, payload) {
            state.general_upload_res[payload.item].ocr_results.data_results[payload.index].text = payload.text;
        },
        templateNameUpdate: function (state, payload) {
            state.templateName = payload;
        },
        generalBoxesUpdate: function (state, payload) {
            state.general_boxes = payload;
        },
        generalImageUpdate: function (state, payload) {
            state.general_upload_image = payload;
        },
        generalImageResponse: function (state, payload) {
            state.general_upload_res = payload;
        },
        generalImageOcrStatus: function (state, payload) {
            state.general_upload_res[payload.item].status = payload.status;
            state.general_upload_res[payload.item].status_msg = payload.status_msg;
            state.general_upload_res[payload.item].file_name = payload.file_name;
            state.general_upload_res[payload.item].series_num = payload.series_num;
        },
        generalImageOcrResults: function (state, payload) {
            state.general_upload_res[payload.item].ocr_results = payload.ocr_results;
            state.general_upload_res[payload.item].file_name = payload.file_name;
            state.general_upload_res[payload.item].series_num = payload.series_num;
        },
        TemplateIdUpdate: function (state, payload) {
            state.template_id = payload;
        },
        createNewUpdate: function (state, payload) {
            state.createNew = payload;
        },
        // setClickedRow(state, { index, value }) {
        //     state.clickedRows[index] = value;
        // },
        // clearClickedRows(state) {
        //     state.clickedRows = {};
        // },
        // deleteClickedRow(state, index) {
        //     delete state.clickedRows[index];
        // }
    },
    actions: {
        updateGeneralImageOcrResults({ commit, state }, { data, image_cv_id }) {
            for (let i = 0; i < state.general_upload_res.length; i++) {
                if (image_cv_id === state.general_upload_res[i].image_id) {
                    for (let j = 0; j < state.general_upload_res[i].ocr_results.data_results.length; j++) {
                        console.log(data[j].annotation.text);
                        commit('GENERAL_IMAGE_OCR_RESULTS_UPDATE', {
                            item: i,
                            index: j,
                            text: data[j].annotation.text
                        });
                    }
                    break;
                }
            }
        },
        updateGeneralImageOcrResultsEdited({ commit, state }, { shape, idx, image_cv_id }) {
            for (let i = 0; i < state.general_upload_res.length; i++) {
                if (image_cv_id === state.general_upload_res[i].image_id) {
                    console.log(shape.name);
                    console.log(state.general_upload_res[i].ocr_results.data_results[idx]);
                        commit('GENERAL_IMAGE_OCR_RESULTS_UPDATE', {
                            item: i,
                            index: idx,
                            text: shape.annotation.text
                        });
                    }
                    break;
                }
        }
    }
});
export default store;
