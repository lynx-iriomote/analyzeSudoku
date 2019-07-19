import SquareCmp from "@/components/parts/SquareCmp.vue";
import Area from "@/data/Area";
import { Component, Prop, Vue } from "vue-property-decorator";
import SudokuUtil from "@/util/SudokuUtil";

/**
 * エリアコンポーネント
 */
@Component({
  components: {
    SquareCmp
  }
})
export default class AreaCmp extends Vue {
  /** フレーム */
  @Prop({ required: true })
  area!: Area;

  /**
   * X座標
   */
  get x(): number {
    return SudokuUtil.areaPosX(this.area.areaId);
  }

  /**
   * Y座標
   */
  get y(): number {
    return SudokuUtil.areaPosY(this.area.areaId);
  }

  /**
   * 装飾
   * @returns クラス名
   */
  get decoration(this: AreaCmp): String {
    if (this.area.areaId % 2 == 0) {
      return "sudoku-area-even";
    } else {
      return "sudoku-area-odd";
    }
  }
}
