import KeyboardKey from "@/const/KeybordKey";
import Flame from "@/data/Flame";
import Square from "@/data/Square";
import { sudokuModule } from "@/store/modules/SudokuModule";
import $ from "jquery";
import { Component, Vue } from "vue-property-decorator";

/**
 * ページの規程クラス
 *
 * [メモ]
 * abnstractクラスにして各Pageで継承させたかったが、
 * @Componentをつけないとライフサイクルハックが出来なく、
 * @Componentをつけるとabstractに出来なかったため、abstractは諦めた
 */
@Component
export default class BasePage extends Vue {
  /**
   * Lifecycle hook mounted
   */
  mounted(): void {
    // イベントアタッチ
    $("#mainContents").on("keydown", this.onKey);
    $("#mainContents").on("click", this.unSelectSqu);
  }

  /**
   * Lifecycle hook beforeDestroy
   */
  beforeDestroy(): void {
    // イベントデタッチ
    $("#mainContents").off("keydown", this.onKey);
    $("#mainContents").off("click", this.unSelectSqu);

    // ページ固有の処理
    this.beforeDestroyUnique();
  }

  /**
   * Lifecycle hook beforeDestroy(ページ固有)
   */
  protected beforeDestroyUnique(): void {}

  /**
   * キーアップイベント時、スキップするかどうか
   * @returns trueでキーイベントをスキップ
   */
  protected get isKeyEventSkip(): boolean {
    return false;
  }

  /**
   * キーイベント
   *
   * @param keyEv キーボードイベント
   */
  private onKey(keyEv: JQuery.KeyboardEventBase) {
    // 通信中はキーイベントスキップ
    if (sudokuModule.connecFlg) {
      return;
    }
    // 固有のスキップ判定
    if (this.isKeyEventSkip) {
      return;
    }
    let isCancel: boolean;
    // alias
    const key: string = keyEv.key;
    switch (keyEv.key) {
      case KeyboardKey.SPACE:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftSpace(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlSpace(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftSpace(key);
        } else {
          isCancel = this.onSpace(key);
        }
        break;

      case KeyboardKey.UP:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftUp(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlUp(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftUp(key);
        } else {
          isCancel = this.onUp(key);
        }
        break;

      case KeyboardKey.DOWN:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftDown(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlDown(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftDown(key);
        } else {
          isCancel = this.onDown(key);
        }
        break;

      case KeyboardKey.RIGHT:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftRight(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlRight(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftRight(key);
        } else {
          isCancel = this.onRight(key);
        }
        break;

      case KeyboardKey.LEFT:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftLeft(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlLeft(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftLeft(key);
        } else {
          isCancel = this.onLeft(key);
        }
        break;

      case KeyboardKey.BACKSPACE:
        if (this.isCtrlShift(keyEv)) {
          isCancel = this.onCtrlShiftBackspace(key);
        } else if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlBackspace(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftBackspace(key);
        } else {
          isCancel = this.onBackspace(key);
        }
        break;

      case KeyboardKey.DELETE:
        if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlDelete(key);
        } else if (this.isShift(keyEv)) {
          isCancel = this.onShiftDelete(key);
        } else {
          isCancel = this.onDelete(key);
        }
        break;

      case KeyboardKey.KEY0:
      // FALL THROUTH
      case KeyboardKey.KEY1:
      // FALL THROUTH
      case KeyboardKey.KEY2:
      // FALL THROUTH
      case KeyboardKey.KEY3:
      // FALL THROUTH
      case KeyboardKey.KEY4:
      // FALL THROUTH
      case KeyboardKey.KEY5:
      // FALL THROUTH
      case KeyboardKey.KEY6:
      // FALL THROUTH
      case KeyboardKey.KEY7:
      // FALL THROUTH
      case KeyboardKey.KEY8:
      // FALL THROUTH
      case KeyboardKey.KEY9:
        const num = parseInt(key, 10);
        // Shift+数字は記号とかになる。
        // 更にOSやキーボードの種類によって変わるため、Shift+数字は未サポート
        if (this.isCtrl(keyEv)) {
          isCancel = this.onCtrlNum(key, num);
        } else {
          isCancel = this.onNum(key, num);
        }
        break;

      default:
        isCancel = false;
        break;
    }
    if (isCancel) {
      keyEv.preventDefault();
    }
  }

  /**
   * 枡の移動
   * @param key 押下されたキー
   */
  protected moveSqu(key: string): void {
    let selectedSqu: Square | undefined | null = sudokuModule.selectedSqu;
    // 枡未選択
    if (!selectedSqu) {
      return;
    }
    // 方向キーで選択枡を移動
    let moveRow = selectedSqu.row;
    let moveClm = selectedSqu.clm;
    if (key == KeyboardKey.UP) {
      moveRow -= 1;
    } else if (key == KeyboardKey.DOWN) {
      moveRow += 1;
    } else if (key == KeyboardKey.RIGHT) {
      moveClm += 1;
    } else {
      moveClm -= 1;
    }

    // 枠外に移動
    if (moveRow < 1 || moveRow > 9 || moveClm < 1 || moveClm > 9) {
      return;
    }
    // 移動先の枡を検索
    const allSquList = sudokuModule.flameToAllSquList.get(this.flame);
    if (!allSquList) {
      throw new TypeError("allSquList is not found");
    }
    selectedSqu = allSquList.find(squ => {
      return squ.row == moveRow && squ.clm == moveClm;
    });
    sudokuModule.selectSqu(selectedSqu);
  }

  /**
   * 枡の選択解除
   */
  protected unSelectSqu() {
    sudokuModule.selectSqu(null);
  }

  /**
   * 枠の取得
   * @returns 枠
   */
  get flame(): Flame {
    throw new TypeError("not override this method");
  }

  // #region キーイベント定義

  /**
   * Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onSpace(key: string): boolean {
    return true;
  }

  /**
   * Ctrl+Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlSpace(key: string): boolean {
    return false;
  }

  /**
   * Shift+Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftSpace(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+Space
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftSpace(key: string): boolean {
    return false;
  }

  /**
   * 上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onUp(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlUp(key: string): boolean {
    return false;
  }

  /**
   * Shift+上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftUp(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+上
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftUp(key: string): boolean {
    return false;
  }

  /**
   * 下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onDown(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlDown(key: string): boolean {
    return false;
  }

  /**
   * Shift+下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftDown(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+下
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftDown(key: string): boolean {
    return false;
  }

  /**
   * 左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onLeft(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlLeft(key: string): boolean {
    return false;
  }

  /**
   * Shift+左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftLeft(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+左
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftLeft(key: string): boolean {
    return false;
  }

  /**
   * 右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onRight(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlRight(key: string): boolean {
    return false;
  }

  /**
   * Shift+右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftRight(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+右
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftRight(key: string): boolean {
    return false;
  }

  /**
   * Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onBackspace(key: string): boolean {
    return false;
  }

  /**
   * Shift+Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftBackspace(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlBackspace(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Shift+Backspace
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlShiftBackspace(key: string): boolean {
    return false;
  }

  /**
   * Delete
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onDelete(key: string): boolean {
    return false;
  }

  /**
   * Shift+Delete
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onShiftDelete(key: string): boolean {
    return false;
  }

  /**
   * Ctrl+Delete
   * @param key キー
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlDelete(key: string): boolean {
    return false;
  }

  /**
   * 数字
   * @param key キー
   * @param num 数字
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onNum(key: string, num: number): boolean {
    return false;
  }

  /**
   * Ctrl+数字
   * @param key キー
   * @param num 数字
   * @returns ブラウザデフォルト動作を停止させる場合はtrueを返却
   */
  protected onCtrlNum(key: string, num: number): boolean {
    return false;
  }

  // #endregion キーイベント

  /**
   * Shiftキー判定
   * @param keyEv キーボードイベント
   */
  private isShift(keyEv: JQuery.KeyboardEventBase): boolean {
    return !keyEv.ctrlKey && keyEv.shiftKey;
  }

  /**
   * Shiftキー判定
   * @param keyEv キーボードイベント
   */
  private isCtrl(keyEv: JQuery.KeyboardEventBase): boolean {
    return keyEv.ctrlKey && !keyEv.shiftKey;
  }

  /**
   * Ctrl+Shiftキー判定
   * @param keyEv キーボードイベント
   */
  private isCtrlShift(keyEv: JQuery.KeyboardEventBase): boolean {
    return keyEv.ctrlKey && keyEv.shiftKey;
  }
}
