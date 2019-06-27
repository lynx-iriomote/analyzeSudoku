<template>
  <g>
    <!-- 記録名 -->
    <text
      :x="startX"
      :y="startY"
      font-size="20"
      dominant-baseline="text-before-edge"
      class="save-text"
    >
      {{ save.saveName }}
    </text>
    <!-- 更新日時 -->
    <text
      :x="startX"
      :y="startY + 30"
      font-size="15"
      dominant-baseline="text-before-edge"
      class="save-text"
    >
      更新日時
    </text>
    <text
      :x="startX"
      :y="startY + 50"
      font-size="15"
      dominant-baseline="text-before-edge"
      class="save-text"
    >
      {{ save.saveDate | yyyymmddhhmmss }}
    </text>

    <!-- ヒント数 -->
    <text
      :x="startX + 170"
      :y="startY + 30"
      font-size="15"
      dominant-baseline="text-before-edge"
      class="save-text"
    >
      ヒント
    </text>
    <text
      :x="startX + 170"
      :y="startY + 50"
      font-size="15"
      dominant-baseline="text-before-edge"
      class="save-text"
    >
      {{ hintQuantity }}&nbsp;個
    </text>

    <!-- クリアボタン -->
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/clear.svg') + '#iconClear'
      }"
      width="30"
      height="30"
      :x="startX + 250"
      :y="startY + 35"
      class="icon-clear"
    />
    <rect
      width="30"
      height="30"
      :x="startX + 250"
      :y="startY + 35"
      fill="white"
      fill-opacity="0"
      @click.stop="clear"
    />

    <!-- 更新ボタン -->
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/update.svg') + '#iconUpdate'
      }"
      width="30"
      height="30"
      :x="startX + 300"
      :y="startY + 35"
      class="icon-default"
    />
    <rect
      width="30"
      height="30"
      :x="startX + 300"
      :y="startY + 35"
      fill="white"
      fill-opacity="0"
      @click.stop="update"
    />

    <!-- 反映ボタン -->
    <use
      v-bind="{
        'xlink:href': require('@/assets/svg/reflect.svg') + '#iconReflect'
      }"
      width="30"
      height="30"
      :x="startX + 350"
      :y="startY + 35"
      class="icon-default"
    />
    <rect
      width="30"
      height="30"
      :x="startX + 350"
      :y="startY + 35"
      fill="white"
      fill-opacity="0"
      @click.stop="reflect"
    />

    <!-- 下線 -->
    <path class="under-line" :d="pathDUnderLine" />
  </g>
</template>

<style lang="scss" scoped>
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

<script lang="ts" src="@/components/parts/ts/SaveModalRowCmp.ts" />
