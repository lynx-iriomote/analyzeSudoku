import SudokuRouterConst from "@/const/SudokuRouterConst";
import router from "@/router";
import InputPage from "@/views/InputPage.vue";
import Vue from "vue";
import Router, { Route } from "vue-router";
import { sudokuModule } from "@/store/modules/SudokuModule";
import { Position } from "vue-router/types/router";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: SudokuRouterConst.INPUT_PATH,
      name: SudokuRouterConst.INPUT_NAME,
      component: InputPage
    },
    {
      path: SudokuRouterConst.ANALYZE_HISTORY_PATH,
      name: SudokuRouterConst.ANALYZE_HISTORY_NAME,
      component: () => import("@/views/AnalyzeHistoryPage.vue"),
      beforeEnter(to: any, from: any, next: any) {
        // 解析履歴がない場合は解析履歴ページに繊維させない
        if (sudokuModule.historyList.length != 0) {
          next();
        } else {
          router.push(SudokuRouterConst.INPUT_PATH);
        }
      }
    }
  ],

  /**
   * スクロール位置の振る舞い
   * @param to TO
   * @param from FROM
   * @param savedPosition 保存されたポジション
   */
  scrollBehavior(to: Route, from: Route, savedPosition: void | Position) {
    // ページ遷移時はトップにスクロール
    return { x: 0, y: 0 };
  }
});
