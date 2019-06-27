<template>
  <g>
    <use
      v-bind="{ 'xlink:href': iconPath }"
      width="32"
      height="32"
      :x="startX + 5"
      :y="startY + 9"
      class="icon"
    />

    <text
      :x="startX + 42"
      :y="startY + 4"
      text-anchor="start"
      dominant-baseline="text-before-edge"
      font-size="12"
      class="ctrl-btn-text-default"
    >
      <tspan>{{ modeLabel }}</tspan>
      <tspan :x="startX + 42" dy="20">モード</tspan>
    </text>

    <rect
      width="88"
      height="48"
      :x="startX + 1"
      :y="startY + 1"
      fill="white"
      fill-opacity="0.0"
      :class="decoration"
      @click.stop="selectMode"
    >
    </rect>
  </g>
</template>

<style lang="scss" scoped>
.ctrl-btn-default {
  stroke: none;
}
.ctrl-btn-selected {
  stroke: $color-line;
  stroke-width: 2;
}
.ctrl-btn-text-default {
  fill: $color-text-default;
  -ms-user-select: none;
  -webkit-user-select: none;
  user-select: none;
}
.icon {
  fill: $color-icon-default;
}
</style>

<script lang="ts" src="@/components/parts/ts/CtrlBtnCmp.ts" />
