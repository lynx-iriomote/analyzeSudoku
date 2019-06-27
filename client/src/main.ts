import App from "@/App.vue";
import router from "@/router";
import store from "@/store/store";
import Vue from "vue";
import VueTouch from "vue-touch";

Vue.use(VueTouch, { name: "v-touch" });

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
