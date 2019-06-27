import Vue from "vue";
import Vuex from "vuex";
import { ISudokuState } from "@/store/modules/SudokuModule";

Vue.use(Vuex);

export interface State {
  sudoku: ISudokuState;
}
export default new Vuex.Store<State>({});
