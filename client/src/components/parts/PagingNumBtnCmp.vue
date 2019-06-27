<template>
  <g>
    <!-- ボタンの枠 -->
    <rect
      width="40"
      height="40"
      :x="startX + 2.5"
      :y="startY + 2.5"
      rx="5"
      ry="5"
      :class="decoration"
    ></rect>

    <!-- 選択状態 -->
    <rect
      v-show="isSelected"
      width="40"
      height="40"
      :x="startX + 2.5"
      :y="startY + 2.5"
      rx="5"
      ry="5"
      class="num-btn-selected"
    ></rect>

    <!-- 数字ボタン -->
    <text
      :x="startX + 22.5"
      :y="startY + 22.5"
      text-anchor="middle"
      dominant-baseline="middle"
      font-size="22"
      :class="textDecoration"
    >
      {{ pagingIdx + 1 }}
    </text>

    <rect
      width="45"
      height="45"
      :x="startX"
      :y="startY"
      rx="5"
      ry="5"
      fill="white"
      fill-opacity="0"
      @click.stop="selectIdx"
    ></rect>
  </g>
</template>

<style lang="scss" scoped>
.num-btn-default {
  stroke: $color-line;
  stroke-width: 1;
}
.num-btn-odd {
  @extend .num-btn-default;
  fill: $color-odd;
}
.num-btn-even {
  @extend .num-btn-default;
  fill: $color-even;
}
.num-btn-disabled {
  @extend .num-btn-default;
  fill: $color-disabled;
  fill-opacity: 0.4;
}
.num-btn-selected {
  @extend .num-btn-default;
  stroke-width: 2;
  fill: $color-selected;
  fill-opacity: 0.6;
}
.num-btn-text-default {
  -ms-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
.num-btn-text-even {
  @extend .num-btn-text-default;
  fill: $color-text-even;
}
.num-btn-text-odd {
  @extend .num-btn-text-default;
  fill: $color-text-odd;
}
svg {
  max-width: 100%;
  height: auto;
}
.icon {
  fill: $color-icon-clear;
}
</style>

<script lang="ts" src="@/components/parts/ts/PagingNumBtnCmp.ts" />
