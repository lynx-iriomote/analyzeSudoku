import { Component, Vue } from "vue-property-decorator";

/**
 * 解析履歴画面用操作マニュアルコンポーネント
 */
@Component
export default class AnalyzeHistoryManualAreaCmp extends Vue {
  /** 展開 */
  expand: boolean = false;

  /**
   * 展開切り替え
   */
  changeExpand(): void {
    this.expand = !this.expand;
  }
}
