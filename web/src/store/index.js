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
        templateName: ''
    },

    mutations: {
        GENERAL_IMAGE_OCR_RESULTS_UPDATE(state, payload) {
            state.general_upload_res[payload.item].ocr_results[payload.index].text = payload.text;
          },
        // recsUpdate: function (state, payload) {
        //     state.selfDefinedRecs[payload.type].push(payload.data);
        // },
        // recsNameUpdate: function (state, payload) {
        //     let index = state.selfDefinedRecs[payload.type].length - 1;
        //     state.selfDefinedRecs[payload.type][index].name = payload.name;
        //     state.selfDefinedRecs[payload.type][index].canDelete = payload.canDelete;
        //     state.selfDefinedRecs[payload.type][index].canEdit = payload.canEdit;
        // },
        // recsSizeUpdate: function (state, payload) {
        //     let index = payload.data.index ? payload.data.index : state.selfDefinedRecs[payload.type].length - 1;
        //     state.selfDefinedRecs[payload.type][index].width = payload.data.width;
        //     state.selfDefinedRecs[payload.type][index].height = payload.data.height;
        //     state.selfDefinedRecs[payload.type][index].endPointX = payload.data.endPointX;
        //     state.selfDefinedRecs[payload.type][index].endPointY = payload.data.endPointY;
        // },
        // recsScaleUpdate: function (state, payload) {
        //     let index = payload.data.index ? payload.data.index : state.selfDefinedRecs[payload.type].length - 1;
        //     state.selfDefinedRecs[payload.type][index].scaleX = payload.data.scaleX;
        //     state.selfDefinedRecs[payload.type][index].scaleY = payload.data.scaleY;
        //     state.selfDefinedRecs[payload.type][index].endPointX = payload.data.endPointX;
        //     state.selfDefinedRecs[payload.type][index].endPointY = payload.data.endPointY;
        //     state.selfDefinedRecs[payload.type][index].startPointX = payload.data.startPointX;
        //     state.selfDefinedRecs[payload.type][index].startPointY = payload.data.startPointY;
        // },
        // recsDelete: function (state, payload) {
        //     state.selfDefinedRecs[payload.type].splice(payload.index, 1);
        // },
        // recsNameEdit: function (state, payload) {
        //     state.selfDefinedRecs[payload.type][payload.index].canSave = payload.canSave;
        //     state.selfDefinedRecs[payload.type][payload.index].canEdit = payload.canEdit;
        // },
        // recsNameSave: function (state, payload) {
        //     state.selfDefinedRecs[payload.type][payload.index].name = payload.name;
        //     state.selfDefinedRecs[payload.type][payload.index].canSave = payload.canSave;
        //     state.selfDefinedRecs[payload.type][payload.index].canEdit = payload.canEdit;
        // },
        // recsClear: function (state) {
        //     Object.keys(state.selfDefinedRecs).forEach((key) => {
        //         state.selfDefinedRecs[key] = [];
        //     });
        // },
        templateNameUpdate: function (state, payload) {
            // state.selfDefinedRecs['name'] = payload;
            state.templateName = payload;
        },
        // templateIdUpdate: function (state, payload) {
        //     state.selfDefinedRecs['id'] = payload;
        // },
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
        },
        generalImageOcrResults: function (state, payload) {
            state.general_upload_res[payload.item].ocr_results = payload.ocr_results;
            state.general_upload_res[payload.item].file_name = payload.file_name;
        },
        TemplateIdUpdate: function (state, payload) {
            state.template_id = payload;
        },
        createNewUpdate: function (state, payload) {
            state.createNew = payload;
        }
    },
    actions: {
        updateGeneralImageOcrResults({ commit, state }, { data, image_cv_id }) {
          for (let i = 0; i < state.general_upload_res.length; i++) {
            if (image_cv_id === state.general_upload_res[i].image_id) {
              for (let j = 0; j < state.general_upload_res[i].ocr_results.length; j++) {
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
      },
});
export default store;
