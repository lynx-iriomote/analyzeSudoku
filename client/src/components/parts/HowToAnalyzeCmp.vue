<template>
  <g :id="isSelected ? 'hilightHowTo' : ''" class="hoho">
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/goSquare.svg') + '#iconGoSquare'
      }"
      width="16"
      height="16"
      :x="startX"
      :y="startY + 3"
      :class="iconDecoration"
    />
    <text
      :x="startX + 21"
      :y="startY"
      font-size="16"
      text-decoration="underline"
      dominant-baseline="text-before-edge"
      :class="textDecoration"
    >
      <tspan
        v-for="(split, idx) in msgSplit"
        :key="idx"
        x="20"
        :dy="idx == 0 ? 0 : 22"
      >
        {{ split }}
      </tspan>
    </text>

    <rect
      :x="startX"
      :y="startY + 3"
      width="445"
      :height="msgSplit.length * 22"
      fill="white"
      fill-opacity="0.0"
      @click.stop="hilightHowTo"
    />
  </g>
</template>

<style lang="scss" scoped>
.hoho {
  position: relative;
}
.how-to-icon-default {
  fill: $color-icon-default;
}
.how-to-icon-selected {
  fill: $color-how-to-changed;
}
.how-to-text-default {
  fill: $color-text-default;
}
.how-to-text-selected {
  fill: $color-how-to-changed;
}
</style>

<script lang="ts" src="@/components/parts/ts/HowToAnalyzeCmp.ts" />
