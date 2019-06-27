import Square from "@/data/Square";
import Flame from "@/data/Flame";
import Region from "@/const/Region";

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
  private static _cnvMapToEnum<T extends Object>(enumObject: T, value: any): T[keyof T] | undefined {
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
}
