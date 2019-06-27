<template>
  <g>
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/pagingPrev.svg') + '#iconPagingPrev'
      }"
      width="32"
      height="32"
      class="icon"
      :x="startX + 6.5"
      :y="startY + 6.5"
    />

    <rect
      width="50"
      height="50"
      :x="startX"
      :y="startY"
      fill="white"
      fill-opacity="0.0"
      @click.stop="pagingPrev"
    />
  </g>
</template>

<style lang="scss" scoped>
.save-modal-btn-text-default {
  fill: $color-text-default;
}

.icon {
  fill: $color-icon-default;
}
</style>

<script lang="ts" src="@/components/parts/ts/PagingPrevBtnCmp.ts" />
