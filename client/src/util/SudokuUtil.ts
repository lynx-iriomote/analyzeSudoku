import Square from "@/data/Square";
import Flame from "@/data/Flame";
import Region from "@/const/Region";
import AnalyzeOption from "@/data/AnalyzeOption";
import Method from "@/const/Method";

/**
 * 数独UTIL
 */
export default class SudokuUtil {
  /**
   * 枠から全ての枡を抽出
   * @param flame 枠
   * @returns 全ての枡
   */
  static findAllSqu(flame: Flame): Square[] {
    const allSquList: Square[] = [];
    flame.areaList.forEach(area => {
      area.squList.forEach(squ => {
        allSquList.push(squ);
      });
    });
    return allSquList;
  }

  /**
   * ランダム文字列生成
   * @returns ランダム文字列
   */
  static createRandomText(): string {
    const RANDOM_LEN: number = 16;
    const CHAR_LIST: string = "abcdefghijklmnopqrstuvwxyz0123456789";
    let random: string = "";
    for (let idx: number = 0; idx < RANDOM_LEN; idx++) {
      random += CHAR_LIST[Math.floor(Math.random() * CHAR_LIST.length)];
    }
    return random;
  }

  /**
   * 指定した文字数でテキストを分解
   * <p>
   * 全角20文字で分割したい場合はcharPerLineに40(半角40文字)を指定すること
   * </p>
   * @param text 分割するテキスト
   * @param charPerLine 一行の文字数(半角文字換算)
   * @returns 分割した文字列
   */
  static splitByCharPerLine(text: string, charPerLine: number): string[] {
    const textList: string[] = [];
    let wkText: string = "";

    let wkLen = 0;
    for (let idx: number = 0; idx < text.length; idx++) {
      const wkChar: string = text[idx];
      if (SudokuUtil.isHalf(wkChar)) {
        // 半角
        wkLen += 1;
      } else {
        wkLen += 2;
      }
      if (charPerLine > wkLen) {
        wkText += wkChar;
      } else if (charPerLine == wkLen) {
        wkText += wkChar;
        textList.push(wkText);
        wkText = "";
        wkLen = 0;
      } else {
        textList.push(wkText);
        wkText = wkChar;
        wkLen = 0;
      }
    }
    if (wkText != "") {
      textList.push(wkText);
    }

    return textList;
  }

  /**
   * 半角判定
   * @param char 判定する文字
   * @returns 半角の場合にtrue
   */
  static isHalf(char: string): boolean {
    return char.match(/^[A-Za-z0-9ｦ-ﾟ]+$/) ? true : false;
  }

  /**
   * 枡を表示テキストに変換
   */
  static squToDispText(squ: Square): string {
    return `行${squ.row}列${squ.clm}`;
  }

  /**
   * ENUM変換
   *
   *
   * 以下のようなことがコンパイルエラーにより出来たかったため、本クラスにメソッドを定義
   *
   * const msgCode: SudokuMsgCode = SudokuMsgCode[json.msgCode]
   *
   * [補足]変数ではなく、リテラルならブラケットでイケる！
   *
   * const msgCode: SudokuMsgCode = SudokuMsgCode["TEST"]
   *
   * 参考URL
   *
   * https://qiita.com/niba1122/items/7bc574b8629dff9ecbb7
   * @param enumObject ENUM
   * @param value 定数名
   * @returns ENUM
   */
  // static cnvMapToEnum<T extends Object>(enumObject: T, value: any): T[keyof T] {
  static cnvMapToEnum<T>(enumObject: T, value: any): T[keyof T] {
    const wk = SudokuUtil._cnvMapToEnum(enumObject, value);
    if (!wk) {
      throw new TypeError(`undefine value=${value}`);
    }
    return wk;
  }

  /**
   * ENUM変換
   *
   *
   * 以下のようなことがコンパイルエラーにより出来たかったため、本クラスにメソッドを定義
   *
   * const msgCode: SudokuMsgCode = SudokuMsgCode[json.msgCode]
   *
   * [補足]変数ではなく、リテラルならブラケットでイケる！
   *
   * const msgCode: SudokuMsgCode = SudokuMsgCode["TEST"]
   *
   * 参考URL
   *
   * https://qiita.com/niba1122/items/7bc574b8629dff9ecbb7
   * @param enumObject ENUM
   * @param value 定数名
   * @returns ENUM
   */
  private static _cnvMapToEnum<T extends Object>(
    enumObject: T,
    value: any
  ): T[keyof T] | undefined {
    if (typeof enumObject === "object") {
      for (const key in enumObject) {
        if (enumObject.hasOwnProperty(key) && enumObject[key] === value) {
          return enumObject[key];
        }
      }
    } else if ((enumObject as any) instanceof Array) {
      return (enumObject as any[]).find(value);
    }
    return undefined;
  }

  /**
   * 領域を文字列に変換
   * @returns 文字列
   */
  static cnvRegionToText(region: Region): string {
    switch (region) {
      case Region.AREA:
        return "エリア";

      case Region.ROW:
        return "行";

      case Region.CLM:
        return "列";

      default:
        throw new TypeError(`not support region ${region}`);
    }
  }

  /**
   * 枡を文字列に変換
   * @param squ 枡
   * @returns 文字列
   */
  static cnvSquToText(squ: Square): string {
    return `行${squ.row}列${squ.clm}`;
  }

  /**
   * 解法をテキストに変換
   * @param method 解法
   * @returns テキスト
   */
  static cnvMethodToText(method: Method): string {
    switch (method) {
      case Method.START:
        return "初期開始";

      case Method.ERROR_CHECK:
        return "エラーチェック";

      case Method.ELIMIONATION:
      // FALL THORUTH
      case Method.ELIMIONATION_ONE_MEMO:
      // FALL THORUTH
      case Method.ELIMIONATION_ONLY_MEMO:
        return "消去法";

      case Method.LOCKED_CANDIDATES:
        return "ロックされた候補法";

      case Method.NAKED_PAIR:
        return "ネイキッドペア法";

      case Method.HIDDEN_PAIR:
        return "隠れペア法";

      case Method.X_WING:
        return "X-Wing法";

      case Method.XY_CHAIN:
        return "XYチェーン法";

      case Method.SIMPLE_CHAIN:
        return "シンプルチェーン法";

      default:
        throw new TypeError(`not support method ${method}`);
    }
  }

  /**
   * テキストの置換
   * @param text 置換対象テキスト
   * @param key 置換対象文字列({key})
   * @param val 置換文字列
   */
  static replaceText(text: string, key: string, val: any): string {
    const regexp = new RegExp(`{${key}}`, "g");
    text = text.replace(regexp, val);
    return text;
  }

  /**
   * エリアのX座標
   * @returns エリアのX座標
   */
  static areaPosX(areaId: number): number {
    switch (areaId) {
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
   * エリアのY座標
   * @returns エリアのY座標
   */
  static areaPosY(areaId: number): number {
    switch (areaId) {
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
   * 枡のX座標
   * @param squ 枡
   * @returns 枡のX座標
   */
  static squarePosX(squ: Square): number {
    switch (squ.squId) {
      case 1:
      // FALL THROUTH
      case 4:
      // FALL THROUTH
      case 7:
        return SudokuUtil.areaPosX(squ.areaId) + 0;

      case 2:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 8:
        return SudokuUtil.areaPosX(squ.areaId) + 50;

      default:
        return SudokuUtil.areaPosX(squ.areaId) + 100;
    }
  }

  /**
   * 枡のY座標
   * @param squ 枡
   * @returns 枡のY座標
   */
  static squarePosY(squ: Square): number {
    switch (squ.squId) {
      case 1:
      // FALL THROUTH
      case 2:
      // FALL THROUTH
      case 3:
        return SudokuUtil.areaPosY(squ.areaId) + 0;

      case 4:
      // FALL THROUTH
      case 5:
      // FALL THROUTH
      case 6:
        return SudokuUtil.areaPosY(squ.areaId) + 50;

      default:
        return SudokuUtil.areaPosY(squ.areaId) + 100;
    }
  }
}
