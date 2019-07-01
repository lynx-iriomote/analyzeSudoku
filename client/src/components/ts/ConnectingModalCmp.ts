import ConnectingCmp from "@/components/parts/ConnectingCmp.vue";
import { Component, Vue } from "vue-property-decorator";

/**
 * 通信中モーダルコンポーネント
 */
@Component({
  components: {
    ConnectingCmp
  }
})
export default class ConnectingModalCmp extends Vue {}
