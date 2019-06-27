<template>
  <g>
    <!-- ボタンの枠 -->
    <circle
      :cx="startX + 22.5"
      :cy="startY + 22.5"
      :class="decoration"
      r="20"
    />

    <!-- 数字ボタン -->
    <text
      v-show="isNotClearBtn"
      :x="startX + 22.5"
      :y="startY + 22.5"
      text-anchor="middle"
      dominant-baseline="middle"
      font-size="22"
      :class="textDecoration"
    >
      {{ num }}
    </text>

    <!-- クリアボタン -->
    <use
      v-show="isClearBtn"
      v-bind="{
        'xlink:href': require('@/assets/svg/clear.svg') + '#iconClear'
      }"
      width="32"
      height="32"
      class="icon"
      :x="startX + 6.5"
      :y="startY + 6.5"
    />

    <!-- 非活性 -->
    <circle
      v-show="isDisabled"
      :cx="startX + 22.5"
      :cy="startY + 22.5"
      r="20"
      class="num-btn-disabled"
    />

    <circle
      :cx="startX + 22.5"
      :cy="startY + 22.5"
      fill="white"
      fill-opacity="0"
      r="20"
      @click.stop="selectNum"
    />
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

<script lang="ts" src="@/components/parts/ts/NumBtnCmp.ts" />
