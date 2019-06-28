<template>
  <g :id="isSelected ? 'hilightHowTo' : ''">
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
#hilightHowTo {
  position: relative;
}

.how-to-icon-selected {
  fill: $color-how-to-changed;
}
.how-to-icon-success {
  fill: $color-msg-success;
}
.how-to-icon-error {
  fill: $color-msg-error;
}
.how-to-icon-info {
  fill: $color-msg-info;
}

.how-to-text-selected {
  fill: $color-how-to-changed;
}
.how-to-text-success {
  fill: $color-msg-success;
}
.how-to-text-error {
  fill: $color-msg-error;
}
.how-to-text-info {
  fill: $color-msg-info;
}
</style>

<script lang="ts" src="@/components/parts/ts/HowToAnalyzeCmp.ts" />
