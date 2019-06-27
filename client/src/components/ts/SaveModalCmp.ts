import SaveModalRowCmp from "@/components/parts/SaveModalRowCmp.vue";
import FlameForStorage from "@/data/FrameForStorage";
import { sudokuModule } from "@/store/modules/SudokuModule";
import MsgFactory from "@/util/MsgFactory";
import _ from "lodash";
import moment from "moment";
import { Component, Emit, Vue } from "vue-property-decorator";

const STORAGE_KEY: string = "flameList";

/**
 * 記録モーダルコンポーネント
 */
@Component({
  components: {
    SaveModalRowCmp
  }
})
export default class SaveModalCmp extends Vue {
  /** 記録名 */
  saveName!: string | null;

  /** ストレージリスト */
  saveList: FlameForStorage[] = [];

  /**
   * Lifecycle hook created
   */
  created(): void {
    this.saveName = null;
    this.saveList.splice(0);
    this.getSaveListFromStorage();
  }

  /**
   * 追加
   */
  add(): void {
    // ストレージ再取得
    this.getSaveListFromStorage();
    let maxId: number | null = this.saveList.reduce((max, save) => {
      return max > save.id ? max : save.id;
    }, 0);

    // ID算出
    if (!maxId) {
      maxId = 0;
    }
    maxId++;

    // 記録名未入力の場合は日時
    if (!this.saveName) {
      this.saveName = moment(new Date()).format("YYYY/MM/DD HH:mm:ss");
    }
    const wkFlameStorage: FlameForStorage = new FlameForStorage(
      maxId,
      sudokuModule.flameForInput,
      this.saveName,
      new Date()
    );
    this.saveList.push(wkFlameStorage);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.saveList));
    this.closeModal();

    // メッセージ
    sudokuModule.addMsg(MsgFactory.createMsgFlameStorageAdd(this.saveName));
  }

  /**
   * ストレージからクリア
   * @param save 記録する枠
   */
  @Emit("clear-save")
  clearSave(save: FlameForStorage): void {
    this.getSaveListFromStorage();
    const afterClearSaveList: FlameForStorage[] = this.saveList.filter(loopSave => {
      return save.id != loopSave.id;
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(afterClearSaveList));
    this.closeModal();

    // メッセージ
    sudokuModule.addMsg(MsgFactory.createMsgFlameStorageClear(save.saveName));
  }

  /**
   * ストレージから更新
   * @param save 記録する枠
   */
  @Emit("update-save")
  updateSave(save: FlameForStorage): void {
    this.getSaveListFromStorage();
    this.saveList.forEach(loopSave => {
      if (save.id == loopSave.id) {
        loopSave.flame = sudokuModule.flameForInput;
        loopSave.saveDate = new Date();
      }
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(this.saveList));
    this.closeModal();

    // メッセージ
    sudokuModule.addMsg(MsgFactory.createMsgFlameStorageUpdate(save.saveName));
  }

  /**
   * ストレージから反映
   * @param save 記録する枠
   */
  @Emit("reflect-save")
  reflectSave(save: FlameForStorage): void {
    sudokuModule.refectFlameToInputFlame(save.flame);
    this.closeModal();

    // メッセージ、解析履歴をクリア
    sudokuModule.clearMsg();
    sudokuModule.clearHistory();

    // メッセージ
    sudokuModule.addMsg(MsgFactory.createMsgFlameStorageReflect(save.saveName));
  }

  /**
   * ローカルストレージから記録リストを取得
   */
  private getSaveListFromStorage(): void {
    if (!(STORAGE_KEY in localStorage)) {
      return;
    }
    let wkSaveList: FlameForStorage[] = JSON.parse(localStorage.getItem(STORAGE_KEY) as string) as FlameForStorage[];
    // 更新日時の降順で並び替える
    wkSaveList = _.orderBy(wkSaveList, "saveDate", "desc");
    this.saveList.splice(0);
    Array.prototype.push.apply(this.saveList, wkSaveList);
  }

  /**
   * モーダルクローズ
   */
  closeModal(): void {
    sudokuModule.hideSaveModalWindow();
  }

  /**
   * SVGのviewbox
   * @returns SVGのviewbox
   */
  get svgVieboxForRow(): string {
    return "0 0 " + this.svgWidthForRow + " " + this.svgHeightForRow;
  }

  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgWidthForRow(): number {
    return 400;
  }
  /**
   * SVGの高さ
   * @returns SVGの高さ
   */
  get svgHeightForRow(): number {
    return this.saveList.length * this.svgHeightForRowPerOne;
  }

  /**
   * 1行の高さ
   * @returns 1行の高さ
   */
  get svgHeightForRowPerOne(): number {
    return 100;
  }
}
