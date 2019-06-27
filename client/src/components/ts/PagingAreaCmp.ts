import BackAnalyzeHistroyBtnCmp from "@/components/parts/BackAnalyzeHistroyBtnCmp.vue";
import PagingNumBtnCmp from "@/components/parts/PagingNumBtnCmp.vue";
import PagingPrevBtnCmp from "@/components/parts/PagingPrevBtnCmp.vue";
import PagingNextBtnCmp from "@/components/parts/PagingNextBtnCmp.vue";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Component, Vue } from "vue-property-decorator";

/**
 * ページングエリアコンポーネント
 */
@Component({
  components: {
    BackAnalyzeHistroyBtnCmp,
    PagingPrevBtnCmp,
    PagingNumBtnCmp,
    PagingNextBtnCmp
  }
})
export default class PagingAreaCmp extends Vue {
  /**
   * 最初のページ(0)を表示するかどうか
   * @returns 最初のページ(0)を表示するかどうか
   */
  get isShowFirstPaging(): boolean {
    return this.pagingIdxList.indexOf(0) < 0;
  }

  get lastPagingIdx(): number {
    return sudokuModule.historyList.length - 1;
  }
  /**
   * 最後のページを表示するかどうか
   * @returns 最後のページを表示するかどうか
   */
  get isShowLastPaging(): boolean {
    return this.pagingIdxList.indexOf(this.lastPagingIdx) < 0;
  }

  /**
   * 画面に表示するページング番号リスト
   * @returns 画面に表示するページング番号リスト
   */
  private get pagingIdxList(): number[] {
    let startIdx: number = sudokuModule.historyIdx - 2;
    let startDiff: number = 0;
    if (startIdx < 0) {
      startDiff = startIdx * -1;
      startIdx = 0;
    }
    let endIdx: number = sudokuModule.historyIdx + 2 + startDiff;
    if (endIdx > sudokuModule.historyList.length - 1) {
      startIdx -= endIdx - sudokuModule.historyList.length + 1;
      if (startIdx < 0) {
        startIdx = 0;
      }
      endIdx = sudokuModule.historyList.length - 1;
    }

    var pagingList: number[] = [];
    for (let wkIdx = startIdx; wkIdx <= endIdx; wkIdx++) {
      pagingList.push(wkIdx);
    }
    return pagingList;
  }

  /**
   * ページングプレビュボタンを表示するかどうか
   * @returns ページングプレビュボタンを表示するかどうか
   */
  get isShowPrevBtn() {
    return sudokuModule.historyIdx != 0;
  }

  /**
   * ページングプレビュボタンを表示するかどうか
   * @returns ページングプレビュボタンを表示するかどうか
   */
  get isShowNextBtn() {
    return sudokuModule.historyIdx != sudokuModule.historyList.length - 1;
  }
}
