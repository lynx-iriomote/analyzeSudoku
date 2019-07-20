import AreaCmp from "@/components/parts/AreaCmp.vue";
import ChainCmp from "@/components/parts/ChainCmp.vue";
import SudokuRouterConst from "@/const/SudokuRouterConst";
import Flame from "@/data/Flame";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 枠コンポーネント
 */
@Component({
  components: {
    AreaCmp,
    ChainCmp
  }
})
export default class FlameCmp extends Vue {
  /** 枠 */
  @Prop({ required: true })
  flame!: Flame;

  /**
   * チェーンを表示するかどうか
   * @requires チェーンを表示するかどうか
   */
  get isChainCmp(): boolean {
    if (this.$route.name == SudokuRouterConst.ANALYZE_HISTORY_NAME) {
      return true;
    }
    return false;
  }
}
