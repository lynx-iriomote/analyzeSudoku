import EditMode from "@/const/EditMode";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Prop, Vue } from "vue-property-decorator";
import moment from "moment";
import FlameForStorage from "@/data/FrameForStorage";

/**
 * 枠コンポーネント
 */
@Component({
  filters: {
    yyyymmddhhmmss(val: Date): string {
      return moment(val).format("YYYY/MM/DD HH:mm:ss");
    }
  }
})
export default class SaveModalRowCmp extends Vue {
  /** 行 */
  @Prop({ required: true })
  save!: FlameForStorage;

  /** 開始X座標 */
  @Prop({ required: true })
  startX!: number;

  /** 開始Y座標 */
  @Prop({ required: true })
  startY!: number;

  /**
   * クリア
   */
  clear(): void {
    this.$emit("clear-save", this.save);
  }

  /**
   * 更新
   */
  update(): void {
    this.$emit("update-save", this.save);
  }

  /**
   * 反映
   */
  reflect(): void {
    this.$emit("reflect-save", this.save);
  }

  /**
   * 下線のd
   * @returns 下線のd
   */
  get pathDUnderLine(): string {
    const startPathX = this.startX;
    const startPathY = this.startY + 75;
    const endPathX = startPathX + 400;
    const endPathY = startPathY;
    return "M" + startPathX + "," + startPathY + " L" + endPathX + "," + endPathY;
  }
  /**
   * ヒント数
   */
  get hintQuantity(): number {
    let hintQuatity = 0;
    this.save.flame.areaList.forEach(area => {
      area.squList.forEach(squ => {
        if (squ.hintVal) {
          hintQuatity++;
        }
      });
    });
    return hintQuatity;
  }
}
