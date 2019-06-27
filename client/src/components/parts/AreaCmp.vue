<template>
  <g>
    <rect :x="x" :y="y" width="150" height="150" :class="decoration"></rect>
    <SquareCmp
      v-for="squ in area.squList"
      :key="squ.squId"
      :area="area"
      :startX="x"
      :startY="y"
      :squ="squ"
    ></SquareCmp>
  </g>
</template>

<style lang="scss" scoped>
.sudoku-area-flamerect {
  stroke: $color-line;
  stroke-width: 2;
}

.sudoku-area-odd {
  @extend .sudoku-area-flamerect;
  fill: $color-odd;
}

.sudoku-area-even {
  @extend .sudoku-area-flamerect;
  fill: $color-even;
}
</style>

<script lang="ts" src="@/components/parts/ts/AreaCmp.ts" />
