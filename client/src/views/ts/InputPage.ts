import BtnAreaCmp from "@/components/BtnAreaCmp.vue";
import FlameCmp from "@/components/FlameCmp.vue";
import InputPageManualAreaCmp from "@/components/InputPageManualAreaCmp.vue";
import MsgAreaCmp from "@/components/MsgAreaCmp.vue";
import SaveModalCmp from "@/components/SaveModalCmp.vue";
import KeyboardKey from "@/const/KeybordKey";
import EditMode from "@/const/EditMode";
import Flame from "@/data/Flame";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Vue } from "vue-property-decorator";
import $ from "jquery";
import BasePage from "@/views/ts/BasePage";

/**
 * 数独ページ
 */
@Component({
  components: {
    FlameCmp,
    InputPageManualAreaCmp,
    BtnAreaCmp,
    SaveModalCmp,
    MsgAreaCmp
  }
})
export default class InputPage extends BasePage {
  /**
   * Lifecycle hook created
   */
  created(): void {
    sudokuModule.init();
  }

  /**
   * フレームの取得
   * @returns フレーム
   * @override
   */
  get flame(): Flame {
    return sudokuModule.flameForInput;
  }

  /**
   * 記録モーダル表示・非表示
   */
  get isSaveModal(): boolean {
    return sudokuModule.saveModalWindow;
  }

  /**
   * メッセージエリア表示・非表示
   */
  get isMsgArea(): boolean {
    return sudokuModule.msgList.length > 0;
  }

  /**
   * キーアップイベント時、スキップするかどうか
   * @returns trueでキーイベントをスキップ
   * @override
   */
  protected get isKeyEventSkip(): boolean {
    // モーダル起動時はキーイベントに触らない
    if (sudokuModule.saveModalWindow) {
      return true;
    }
    return false;
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
   * Shift+上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftUp(key: string): boolean {
    this.changeMode(key);
    return true;
  }

  /**
   * Shift+下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftDown(key: string): boolean {
    this.changeMode(key);
    return true;
  }

  /**
   * Shift+左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftLeft(key: string): boolean {
    this.changeMode(key);
    return true;
  }

  /**
   * Shift+右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   * @override
   */
  protected onShiftRight(key: string): boolean {
    this.changeMode(key);
    return true;
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
   * 数字
   * @param key キー
   * @param num 数字
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onNum(key: string, num: number): boolean {
    if (!sudokuModule.selectedSqu) {
      return false;
    }
    if (num == 0) {
      return this.clearSquVal();
    }
    sudokuModule.updateSelectedSquVal(num);
    return true;
  }

  /**
   * Delete
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onDelete(key: string): boolean {
    return this.clearSquVal();
  }

  /**
   * Shift+Delete
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftDelete(key: string): boolean {
    return this.clearSquVal();
  }

  /**
   * Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onBackspace(key: string): boolean {
    return this.clearSquVal();
  }

  /**
   * Shift+Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftBackspace(key: string): boolean {
    return this.clearSquVal();
  }

  /**
   * 枡クリア
   * @returns true固定
   */
  private clearSquVal(): boolean {
    sudokuModule.updateSelectedSquVal(null);
    return true;
  }

  /**
   * モード切り替え
   * @param key 押下されたキー
   */
  private changeMode(key: string): void {
    if (key == KeyboardKey.RIGHT || key == KeyboardKey.DOWN) {
      // Shift+下、右押下時は以下のようにモードを切り替える
      // HINT -> VAL -> MEMO -> HINT ...
      switch (sudokuModule.editMode) {
        case EditMode.HINT:
          sudokuModule.changeEditMode(EditMode.VAL);
          break;
        case EditMode.VAL:
          sudokuModule.changeEditMode(EditMode.MEMO);
          break;
        case EditMode.MEMO:
          sudokuModule.changeEditMode(EditMode.HINT);
          break;

        default:
          throw new TypeError("unsupport editMode=" + sudokuModule.editMode);
      }
    } else {
      // Shift+上、左押下時は以下のようにモードを切り替える
      // HINT <- VAL <- MEMO <- HINT ...
      switch (sudokuModule.editMode) {
        case EditMode.HINT:
          sudokuModule.changeEditMode(EditMode.MEMO);
          break;
        case EditMode.MEMO:
          sudokuModule.changeEditMode(EditMode.VAL);
          break;
        case EditMode.VAL:
          sudokuModule.changeEditMode(EditMode.HINT);
          break;

        default:
          throw new TypeError("unsupport editMode=" + sudokuModule.editMode);
      }
    }
  }
}
