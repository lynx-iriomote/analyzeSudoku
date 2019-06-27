import SquareCmp from "@/components/parts/SquareCmp.vue";
import Area from "@/data/Area";
import { Component, Prop, Vue } from "vue-property-decorator";

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
    switch (this.area.areaId) {
      case 1:
      // FALL THROUTH
      case 4:
      // FALL THROUTH
      case 7:
        return 0;

      case 2:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 8:
        return 150;

      default:
        return 300;
    }
  }

  /**
   * Y座標
   */
  get y(): number {
    switch (this.area.areaId) {
      case 1:
      // FALL THROUTH
      case 2:
      // FALL THROUTH
      case 3:
        return 0;

      case 4:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 6:
        return 150;

      default:
        return 300;
    }
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
