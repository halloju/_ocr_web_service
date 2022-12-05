import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate'

const store = new Vuex.Store({
  plugins: [createPersistedState()],
  state: {
    // 預設 loaded 為 false
    cus_input : {
                "AP15": 0,
                "ST07": 0,
                "EE62": 0,
                "ET31": 0,
                "A394": 0,
                "BB74": 0,
                "E441": 0,
                "AG01": 0
                },
    event: "",
    response: {},
    recs_text: [],
    recs_block: [],
    recs_mask: [],
  },

  mutations: {
    step1:function (state, payload) {
        state.cus_input = payload;
    },
    step3:function (state, payload) {
        state.event = payload
    },
    sendAPI:function (state, payload) {
        state.response = payload
    },
    back:function (state) {
        state.cus_input = {
          "AP15": 0,
          "ST07": 0,
          "EE62": 0,
          "ET31": 0,
          "A394": 0,
          "BB74": 0,
          "E441": 0,
          "AG01": 0
          },
        state.event = "",
        state.response = {}
    }
  },
})
export default store;
