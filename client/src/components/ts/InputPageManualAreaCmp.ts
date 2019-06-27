import { Component, Vue } from "vue-property-decorator";

/**
 * 入力画面用操作マニュアルコンポーネント
 */
@Component
export default class InputPageManualAreaCmp extends Vue {
  /** 展開 */
  expand: boolean = false;

  /**
   * 展開切り替え
   */
  changeExpand(): void {
    this.expand = !this.expand;
  }
}
