<template>
  <div class="sudoku-frame">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      version="1.1"
      viewBox="-1 -1 452 452"
      width="450"
      height="450"
    >
      <AreaCmp v-for="area in flame.areaList" :key="area.areaId" :area="area" />

      <rect
        x="0"
        y="0"
        width="450"
        height="450"
        fill="none"
        stroke="black"
        stroke-width="2"
        class="sudoku-flame-flamerect"
      />
    </svg>
  </div>
</template>

<style lang="scss" scoped>
.sudoku-frame {
  min-width: 300px;
  max-width: 450px;
  height: auto;
  padding-top: 5px;
  margin: auto;
}
.sudoku-flame-flamerect {
  stroke: $color-line;
}
</style>

<script lang="ts" src="@/components/ts/FlameCmp.ts" />
