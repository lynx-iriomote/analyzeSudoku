<template>
  <div class="sudoku-btn-area">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1"
      viewBox="0 0 450 50"
      width="450"
      height="50"
    >
      <!-- 戻るボタン -->
      <BackAnalyzeHistroyBtnCmp :startX="0" :startY="0" />
      <!-- 最初のページボタン -->
      <PagingNumBtnCmp
        v-show="isShowFirstPaging"
        :startX="45"
        :startY="0"
        :pagingIdx="0"
        :pos="0"
      />
      <!-- prevボタン -->
      <PagingPrevBtnCmp v-show="isShowPrevBtn" :startX="90" :startY="0" />
      <!-- ページボタン -->
      <PagingNumBtnCmp
        v-for="(pageIdx, loopIdx) in pagingIdxList"
        :key="pageIdx"
        :startX="135 + loopIdx * 45"
        :startY="0"
        :pagingIdx="pageIdx"
        :pos="loopIdx + 1"
      />
      <!-- nextボタン -->
      <PagingNextBtnCmp
        v-show="isShowNextBtn"
        :startX="135 + pagingIdxList.length * 45"
        :startY="0"
      />
      <!-- 最後のページボタン -->
      <PagingNumBtnCmp
        v-show="isShowLastPaging"
        :startX="180 + pagingIdxList.length * 45"
        :startY="0"
        :pagingIdx="lastPagingIdx"
        :pos="pagingIdxList.length + 1"
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

<script lang="ts" src="@/components/ts/PagingAreaCmp.ts" />
