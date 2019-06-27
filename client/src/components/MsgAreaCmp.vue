<template>
  <div class="msg-area" :style="{ height: msgAreaMsgHeight }">
    <div class="msg-area-msg" id="msgAreaMsg">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        :viewBox="svgViebox"
        :width="svgWidth"
        :height="svgHeight"
      >
        <!-- メッセージ -->
        <g
          v-for="msg in msgList"
          :key="msg.id"
          :id="isLastMsg(msg) ? 'lastMsg' : ''"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/msg.svg') + '#iconMsg'
            }"
            width="16"
            height="16"
            x="3"
            :y="svgTextY(msg) + 7"
            :class="decoration(msg)"
          />
          <text
            x="24"
            :y="svgTextY(msg) + 5"
            font-size="16"
            dominant-baseline="text-before-edge"
            :class="decoration(msg)"
          >
            <tspan
              v-for="(split, splitIdx) in msgSplit(msg)"
              :key="splitIdx"
              x="20"
              :dy="splitIdx == 0 ? 0 : 20"
              :id="
                isLastMsg(msg, splitIdx, msgSplit(msg).length) ? 'lastMsg' : ''
              "
            >
              {{ split }}
            </tspan>
          </text>
        </g>
      </svg>
    </div>

    <div class="msg-area-btn">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        viewBox="0 0 50 100"
        width="50"
        height="100"
      >
        <!-- クリアボタン -->
        <use
          v-show="isClearBtn"
          v-bind="{
            'xlink:href': require('@/assets/svg/clear.svg') + '#iconClear'
          }"
          width="32"
          height="32"
          x="2"
          y="2"
          class="icon-clear"
        />
        <rect
          v-show="isClearBtn"
          width="32"
          height="32"
          x="2"
          y="2"
          fill="white"
          fill-opacity="0"
          @click.stop="clearMsg"
        />

        <!-- 拡大ボタン -->
        <use
          v-show="isDoBigBtn"
          v-bind="{
            'xlink:href': require('@/assets/svg/doBig.svg') + '#iconDoBig'
          }"
          width="32"
          height="32"
          x="2"
          y="40"
          class="icon-default"
        />
        <rect
          v-show="isDoBigBtn"
          width="32"
          height="32"
          x="2"
          y="40"
          fill="white"
          fill-opacity="0"
          @click.stop="doBigMsgArea"
        />

        <!-- 縮小ボタン -->
        <use
          v-show="isDoSmallBtn"
          v-bind="{
            'xlink:href': require('@/assets/svg/doSmall.svg') + '#iconDoSmall'
          }"
          width="32"
          height="32"
          x="2"
          y="40"
          class="icon-default"
        />
        <rect
          v-show="isDoSmallBtn"
          width="32"
          height="32"
          x="2"
          y="40"
          fill="white"
          fill-opacity="0"
          @click.stop="doSmallMsgArea"
        />
      </svg>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#lastMsg {
  position: relative;
}
.icon-default {
  fill: $color-icon-default;
}
.icon-clear {
  fill: $color-icon-clear;
}

.msg-area {
  display: grid;
  gap: 5px;
  grid-template-columns: 410px 35px;
  padding-top: 10px;
  padding-bottom: 10px;
  min-width: 300px;
  max-width: 450px;
  height: auto;
  margin: auto;
  .msg-area-msg {
    position: relative;
    border: solid 1px $color-line;
    overflow-y: auto;
    overflow-x: hidden;
  }
}
.msg-text-success {
  fill: $color-msg-success;
}
.msg-text-error {
  fill: $color-msg-error;
}
.msg-text-info {
  fill: $color-msg-info;
}
</style>

<script lang="ts" src="@/components/ts/MsgAreaCmp.ts" />
