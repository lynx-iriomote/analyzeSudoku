<template>
  <g>
    <!-- 枡 -->
    <rect :x="x" :y="y" width="50" height="50" :class="decoration"></rect>

    <!-- エラー -->
    <path
      v-show="squ.errorList.length > 0"
      :d="errorPathD"
      class="error-bg"
    ></path>

    <!-- 値 -->
    <text
      v-show="squ.hintVal || squ.val"
      :x="x + 25"
      :y="y + 25"
      text-anchor="middle"
      dominant-baseline="central"
      font-size="32"
      :class="textDecoration"
      >{{ dispVal }}</text
    >

    <!-- 初期値の場合は左上にアイコン -->
    <use
      v-show="squ.hintVal"
      v-bind="{
        'xlink:href': require('@/assets/svg/hint.svg') + '#iconHint'
      }"
      width="12"
      height="12"
      :x="x + 2"
      :y="y + 2"
      :class="initIconDecoration"
    />

    <!-- メモ -->
    <text
      v-for="memo in squ.memoValList"
      :key="memo"
      :x="memoX(memo) + 9"
      :y="memoY(memo) + 10"
      text-anchor="middle"
      dominant-baseline="middle"
      font-size="15"
      :class="memoTextDecoration(memo)"
      >{{ memo }}</text
    >

    <rect
      :x="x"
      :y="y"
      width="50"
      height="50"
      fill="white"
      fill-opacity="0"
      @click.stop="selectSqu"
    ></rect>
  </g>
</template>

<style lang="scss" scoped>
////////////////
// 背景色
////////////////
.square-bg-default {
  fill: none;
  stroke: $color-line;
  stroke-width: 1;
}
.square-bg-odd-hilight {
  @extend .square-bg-default;
  fill: $color-odd-hilight;
}
.square-bg-odd-selected {
  @extend .square-bg-default;
  fill: $color-odd-selected;
}
.square-bg-even-hilight {
  @extend .square-bg-default;
  fill: $color-even-hilight;
}
.square-bg-even-selected {
  @extend .square-bg-default;
  fill: $color-even-selected;
}

.square-bg-how-to-changed {
  @extend .square-bg-default;
  fill: $color-how-to-changed;
}
.square-bg-how-to-trigger {
  @extend .square-bg-default;
  fill: $color-how-to-trigger;
}

.error-bg {
  stroke: $color-icon-error;
  stroke-width: 1;
  fill: none;
}

////////////////
// アイコン
////////////////
.init-icon-even {
  fill: $color-icon-even;
}
.init-icon-odd {
  fill: $color-icon-odd;
}

////////////////
// 文字色
////////////////
.square-text-default {
  font-weight: normal;
  fill: $color-text-default;
  -ms-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
.square-text-odd {
  @extend .square-text-default;
  fill: $color-text-odd;
}
.square-text-even {
  @extend .square-text-default;
  fill: $color-text-even;
}
.square-text-hilight {
  @extend .square-text-default;
  font-weight: bolder;
  fill: $color-text-hilight;
}
</style>

<script lang="ts" src="@/components/parts/ts/SquareCmp.ts" />
