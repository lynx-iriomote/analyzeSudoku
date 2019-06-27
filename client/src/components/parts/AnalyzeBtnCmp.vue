<template>
  <g>
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/analyze.svg') + '#iconAnalyze'
      }"
      width="32"
      height="32"
      class="icon"
      :x="startX + 5"
      :y="startY + 9"
    />
    <text
      :x="startX + 42"
      :y="startY + 4"
      text-anchor="start"
      dominant-baseline="text-before-edge"
      font-size="12"
      class="analyze-btn-text-default"
    >
      <tspan>解く</tspan>
    </text>

    <rect
      width="88"
      height="48"
      :x="startX + 1"
      :y="startY + 1"
      fill="white"
      fill-opacity="0.0"
      @click.stop="analyze"
    />
  </g>
</template>

<style lang="scss" scoped>
.analyze-btn-text-default {
  fill: $color-text-default;
  -ms-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
.icon {
  fill: $color-icon-default;
}
</style>

<script lang="ts" src="@/components/parts/ts/AnalyzeBtnCmp.ts" />
