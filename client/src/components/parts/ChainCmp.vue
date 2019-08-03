<template>
  <g v-if="chainSquList" id="chainCmp">
    <path id="chainPath" :d="chainLine" />
    <use
      v-bind="{
        'xlink:href':
          require('@/assets/svg/chainFollow.svg') + '#iconChainFollow'
      }"
      width="32"
      height="32"
      class="icon-chain-follow"
    >
      <animateMotion
        :path="chainLineFollowPath"
        begin="0s"
        :dur="chainLineFollowDur"
        :keyPoints="chainLineFollowKeyPoints"
        :keyTimes="chainLineFollowKeyTimes"
        calcMode="linear"
        repeatCount="indefinite"
      />
    </use>
  </g>
</template>

<style lang="scss" scoped>
.icon-chain-follow {
  fill: $color-chain-line-follow;
}

#chainPath {
  stroke: $color-chain-line;
  stroke-width: 10px;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>

<script lang="ts" src="@/components/parts/ts/ChainCmp.ts" />
