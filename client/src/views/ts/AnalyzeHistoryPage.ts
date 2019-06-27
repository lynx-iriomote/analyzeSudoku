import FlameCmp from "@/components/FlameCmp.vue";
import AnalyzeHistoryManualAreaCmp from "@/components/AnalyzeHistoryManualAreaCmp.vue";
import HowToAnalyzeAreaCmp from "@/components/HowToAnalyzeAreaCmp.vue";
import MsgAreaCmp from "@/components/MsgAreaCmp.vue";
import PagingAreaCmp from "@/components/PagingAreaCmp.vue";
import KeyboardKey from "@/const/KeybordKey";
import Flame from "@/data/Flame";
import HowToAnalyze from "@/data/HowToAnalyze";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Vue } from "vue-property-decorator";
import Square from "@/data/Square";
import BasePage from "@/views/ts/BasePage";

/**
 * 解析履歴ページ
 */
@Component({
  components: {
    AnalyzeHistoryManualAreaCmp,
    FlameCmp,
    PagingAreaCmp,
    HowToAnalyzeAreaCmp,
    MsgAreaCmp
  }
})
export default class AnalyzeHistoryPage extends BasePage {
  /**
   * メッセージエリア表示・非表示
   */
  get isMsgArea(): boolean {
    return sudokuModule.msgList.length > 0;
  }

  /**
   * フレームの取得
   * @returns フレーム
   * @override
   */
  get flame(): Flame {
    return sudokuModule.historyList[sudokuModule.historyIdx].flame;
  }

  /**
   * 解析方法リスト
   */
  get howToList(): HowToAnalyze[] {
    return sudokuModule.historyList[sudokuModule.historyIdx].howToAnalyzeList;
  }

  /**
   * ハイライトする解析履歴IDX
   */
  get hilightHowToIdx(): number | null {
    return sudokuModule.hilightHowToIdx;
  }

  /**
   * Shift+Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftSpace(key: string): boolean {
    return this.onSpaceUnique();
  }

  /**
   * Shift+Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onSpace(key: string): boolean {
    return this.onSpaceUnique();
  }

  /**
   * 枡の選択、未選択の切り替え
   * @returns true固定
   */
  private onSpaceUnique(): boolean {
    // 枡未選択→選択
    if (!sudokuModule.selectedSqu) {
      sudokuModule.selectSquDefault(this.flame);
    }
    // 枡選択→未選択
    else {
      sudokuModule.selectSqu(null);
    }
    return true;
  }

  /**
   * 上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onUp(key: string): boolean {
    return this.moveSquWrap(key);
  }

  /**
   * 下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onDown(key: string): boolean {
    return this.moveSquWrap(key);
  }

  /**
   * 左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onLeft(key: string): boolean {
    return this.moveSquWrap(key);
  }

  /**
   * 右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onRight(key: string): boolean {
    return this.moveSquWrap(key);
  }

  /**
   * 枡移動ラップメソッド
   * @param key キー
   * @returns 枡移動時はtrue、移動しない場合はfalse
   */
  private moveSquWrap(key: string): boolean {
    if (!sudokuModule.selectedSqu) {
      return false;
    }
    this.moveSqu(key);
    return true;
  }

  /**
   * Shift+上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftUp(key: string): boolean {
    // 前の解析履歴をハイライト
    sudokuModule.moveBackHowto();
    return true;
  }

  /**
   * Shift+下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftDown(key: string): boolean {
    // 次の解析履歴をハイライト
    sudokuModule.moveNextHowto();
    return true;
  }

  /**
   * Shift+左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftLeft(key: string): boolean {
    this.moveBackHistory();
    return true;
  }

  /**
   * Shift+右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftRight(key: string): boolean {
    this.moveNextHistory();
    return true;
  }

  /**
   * 前の履歴を表示
   */
  private moveBackHistory(): void {
    sudokuModule.moveBackHistory();
  }

  /**
   * 次の履歴を表示
   */
  private moveNextHistory(): void {
    sudokuModule.moveNextHistory();
  }
}
