<template>
  <div class="input-manual-area">
    <div v-show="!expand" @click.stop="changeExpand" key="expand">
      <span>簡易操作マニュアルを表示</span>
    </div>
    <div v-show="expand">
      <span @click="changeExpand">簡易操作マニュアルを非表示</span>
      <h2>解析方法履歴画面</h2>
      <p class="p1">
        解析方法履歴画面とは…数独をどのように解析したか表示するページ
      </p>

      <h3>履歴移動</h3>
      <p class="p2">
        数字を選択、または
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href':
                require('@/assets/svg/pagingPrev.svg') + '#iconPagingPrev'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタン、
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href':
                require('@/assets/svg/pagingNext.svg') + '#iconPagingNext'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタンを押下
      </p>

      <h3>解読方法のハイライト切替え</h3>
      <p class="p2">
        ハイライトしたい
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href':
                require('@/assets/svg/goSquare.svg') + '#iconGoSquare'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>

        <span style="text-decoration: underline">解析方法</span>を押下
      </p>

      <h3>数独入力画面に戻る</h3>
      <p class="p2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/back.svg') + '#iconBack'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタンを押下
      </p>

      <h2>キーボードショートカット</h2>
      <h3>方向キー</h3>
      <p class="p2">枡移動</p>
      <h3>スペース</h3>
      <p class="p2">枡の選択・選択解除</p>
      <h3>Shift+左キー</h3>
      <p class="p2">前の履歴に移動</p>
      <h3>Shift+右キー</h3>
      <p class="p2">次の履歴に移動</p>
      <h3>Shift+下キー</h3>
      <p class="p2">次の解析方法をハイライト</p>
      <h3>Shift+上キー</h3>
      <p class="p2">前の解析方法をハイライト</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.icon-default {
  fill: $color-icon-default;
}

.icon-clear {
  fill: $color-icon-clear;
}

.input-manual-area {
  min-width: 300px;
  max-width: 450px;
  height: auto;
  padding-top: 5px;
  padding-bottom: 5px;
  margin: auto;
  color: $color-text-default;
  font-size: 16px;
  p {
    padding-left: 0px;
  }
  h2 {
    padding-left: 0px;
    font-size: 20px;
  }
  .p1 {
    padding-left: 20px;
  }
  h3 {
    padding-left: 20px;
  }
  .p2 {
    padding-left: 40px;
  }
  .p3 {
    padding-left: 60px;
  }
}
</style>

<script lang="ts" src="@/components/ts/AnalyzeHistoryManualAreaCmp.ts" />
