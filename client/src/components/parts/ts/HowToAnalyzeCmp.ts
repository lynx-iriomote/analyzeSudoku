import MsgType from "@/const/MsgType";
import HowToAnalyze from "@/data/HowToAnalyze";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 解析方法コンポーネント
 */
@Component
export default class HowToAnalyzeCmp extends Vue {
  /** 解析方法 */
  @Prop({ required: true })
  howTo!: HowToAnalyze;

  /** 分割文字列 */
  @Prop({ required: true })
  msgSplit!: string[];

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * テキストの装飾
   * @returns クラス名
   */
  get textDecoration(): string {
    if (this.isSelected) {
      return "how-to-text-selected";
    }
    switch (this.howTo.msg.msgType) {
      case MsgType.INFO:
        return "how-to-text-info";

      case MsgType.SUCCESS:
        return "how-to-text-success";

      case MsgType.ERROR:
        return "how-to-text-error";

      default:
        throw new TypeError(`not support msgType ${this.howTo.msg.msgType}`);
    }
  }

  /**
   * アイコンの装飾
   * @returns クラス名
   */
  get iconDecoration(): string {
    if (this.isSelected) {
      return "how-to-icon-selected";
    }
    switch (this.howTo.msg.msgType) {
      case MsgType.INFO:
        return "how-to-icon-info";

      case MsgType.SUCCESS:
        return "how-to-icon-success";

      case MsgType.ERROR:
        return "how-to-icon-error";

      default:
        throw new TypeError(`not support msgType ${this.howTo.msg.msgType}`);
    }
  }

  /**
   * 解析方法が選択されているかどうか
   * @returns 解析方法が選択されているかどうか
   */
  get isSelected(): boolean {
    return (
      this.howTo ==
      sudokuModule.historyList[sudokuModule.historyIdx].howToAnalyzeList[
        sudokuModule.hilightHowToIdx!
      ]
    );
  }

  /**
   * 解析方法をハイライト
   */
  hilightHowTo(): void {
    sudokuModule.changeHilightHowTo(this.howTo);
  }
}
