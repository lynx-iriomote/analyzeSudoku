<template>
  <g>
    <!-- checkbox -->
    <use
      v-bind="{
        'xlink:href':
          require('@/assets/svg/checkBoxFlame.svg') + '#iconCheckBoxFlame'
      }"
      width="32"
      height="32"
      :class="checkboxFlameDecoration"
      :x="startX"
      :y="startY + 9"
    />
    <use
      v-show="analyzeOption.check"
      v-bind="{
        'xlink:href':
          require('@/assets/svg/checkBoxCheck.svg') + '#iconCheckBoxCheck'
      }"
      width="32"
      height="32"
      class="icon-checkbox-check"
      :x="startX"
      :y="startY + 9"
    />
    <rect
      width="50"
      height="50"
      :x="startX"
      :y="startY"
      fill="white"
      fill-opacity="0"
      @click.stop="check"
    />

    <!-- テキスト -->
    <text
      :x="startX + 40"
      :y="startY + 12"
      font-size="20"
      dominant-baseline="text-before-edge"
      :class="textDecoration"
      @click.stop="check"
    >
      {{ analyzeOption.text }}
    </text>
  </g>
</template>

<style lang="scss" scoped>
.icon-checkbox-flame-default {
  fill: none;
}
.icon-checkbox-flame-check {
  @extend .icon-checkbox-flame-default;
  stroke: $color-checkbox-check;
}
.icon-checkbox-flame-uncheck {
  @extend .icon-checkbox-flame-default;
  stroke: $color-checkbox-uncheck;
}
.icon-checkbox-flame-disabled {
  @extend .icon-checkbox-flame-default;
  stroke: $color-checkbox-disabled;
}

.icon-checkbox-check {
  fill: $color-checkbox-check;
}
.icon-checkbox-uncheck {
  fill: $color-checkbox-uncheck;
}
.icon-checkbox-disabled {
  fill: $color-checkbox-disabled;
}

.save-text {
  fill: $color-text-default;
}

.icon-default {
  fill: $color-icon-default;
}

.icon-clear {
  fill: $color-icon-clear;
}
.under-line {
  stroke: $color-line;
  stroke-width: 1;
  stroke-dasharray: 24 3 2 3 2 3;
  fill: none;
}
</style>

<script lang="ts" src="@/components/parts/ts/AnalyzeOptionRowCmp.ts" />
