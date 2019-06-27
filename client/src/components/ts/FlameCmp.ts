import AreaCmp from "@/components/parts/AreaCmp.vue";
import Flame from "@/data/Flame";
import { Component, Prop, Vue } from "vue-property-decorator";

/**
 * 枠コンポーネント
 */
@Component({
  components: {
    AreaCmp
  }
})
export default class FlameCmp extends Vue {
  /** 枠 */
  @Prop({ required: true })
  flame!: Flame;
}
