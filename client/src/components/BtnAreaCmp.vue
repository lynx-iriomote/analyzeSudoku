<template>
  <div class="sudoku-btn-area">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1"
      :viewBox="svgViewPost"
      :width="svgWidth"
      :height="svgHeight"
    >
      <!-- 数字ボタン -->
      <NumBtnCmp
        v-for="num in 10"
        :key="num"
        :num="num"
        :startX="(num - 1) * 45"
        :startY="0"
      />

      <!-- 初期値モード -->
      <CtrlBtnCmp :editMode="editModeHint" :startX="0" :startY="50" />

      <!-- 値モード -->
      <CtrlBtnCmp :editMode="editModeVal" :startX="90" :startY="50" />

      <!-- メモモード -->
      <CtrlBtnCmp :editMode="editModeMemo" :startX="180" :startY="50" />

      <!-- 解く -->
      <AnalyzeBtnCmp :startX="270" :startY="50" />

      <!-- 記録 -->
      <SaveModalBtnCmp :startX="360" :startY="50" />

      <!-- 解析履歴表示 -->
      <GoAnalyzeHistroyBtnCmp
        v-if="isShowGoAnalyzeHistoryBtn"
        :startX="360"
        :startY="100"
      />
    </svg>
  </div>
</template>

<style lang="scss" scoped>
.sudoku-btn-area {
  padding-top: 5px;
  min-width: 300px;
  max-width: 450px;
  height: auto;
  margin: auto;
}
</style>

<script lang="ts" src="@/components/ts/BtnAreaCmp.ts" />
