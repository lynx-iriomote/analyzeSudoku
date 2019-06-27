<template>
  <div class="input-manual-area">
    <div v-show="!expand" @click.stop="changeExpand" key="expand">
      <span>簡易操作マニュアルを表示</span>
    </div>
    <div v-show="expand">
      <span @click="changeExpand">簡易操作マニュアルを非表示</span>
      <h2>数独入力画面の操作</h2>
      <p class="p1">数独入力画面とは…数独を入力するページ</p>

      <h3>数字入力方法</h3>
      <p class="p2">枡を選択し、数字ボタンを入力</p>

      <h3>数字入力削除</h3>
      <p class="p2">
        枡を選択し、
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/clear.svg') + '#iconClear'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-clear"
          /></svg
        >ボタンを押下
      </p>

      <h3>入力モード切替え</h3>
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
              'xlink:href': require('@/assets/svg/hint.svg') + '#iconHint'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          /></svg
        >ヒントボタン、
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/pen.svg') + '#iconPen'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          /></svg
        >値モードボタン、
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/memo.svg') + '#iconMemo'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          /></svg
        >メモモードボタンを押下
      </p>

      <h3>入力した数独を解析する</h3>
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
              'xlink:href': require('@/assets/svg/analyze.svg') + '#iconAnalyze'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        解析ボタンを押下、しばらく待つと解析結果が数独入力画面に反映される
      </p>

      <h2>記録画面の操作</h2>
      <p class="p1">記録画面とは…入力した数独を保存、呼出しを行うする画面</p>

      <h3>表示方法</h3>
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
              'xlink:href': require('@/assets/svg/save.svg') + '#iconSave'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        記録ボタンを押下すると記録画面が表示される
      </p>

      <h3>入力した数独を記録する</h3>
      <p class="p2">
        記録名を入力、
        <svg
          xmlns="http://www.w3.org/2000/svg"
          version="1.1"
          viewBox="0 0 16 16"
          width="16"
          height="16"
        >
          <use
            v-bind="{
              'xlink:href': require('@/assets/svg/plus.svg') + '#iconPlus'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタン押下でブラウザに記録される。
      </p>

      <h3>記録した数独を呼出す</h3>
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
              'xlink:href': require('@/assets/svg/reflect.svg') + '#iconReflect'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタン押下で記録した数独が反映される
      </p>

      <h3>記録した数独を更新する</h3>
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
              'xlink:href': require('@/assets/svg/update.svg') + '#iconUpdate'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-default"
          />
        </svg>
        ボタン押下で記録した数独が数独入力画面の内容で上書きされる
      </p>

      <h3>記録した数独を削除する</h3>
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
              'xlink:href': require('@/assets/svg/clear.svg') + '#iconClear'
            }"
            width="16"
            height="16"
            x="0"
            y="0"
            class="icon-clear"
          />
        </svg>
        ボタン押下で記録した数独が削除される
      </p>

      <h2>キーボードショートカット</h2>
      <h3>方向キー</h3>
      <p class="p2">枡移動</p>
      <h3>Shift+方向キー</h3>
      <p class="p2">入力モード切替え</p>
      <h3>数字キー</h3>
      <p class="p2">数字を入力(0で削除)</p>
      <h3>Delete・Backspace</h3>
      <p class="p2">入力した数字を削除</p>
      <h3>スペース</h3>
      <p class="p2">枡の選択・選択解除</p>
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

<script lang="ts" src="@/components/ts/InputPageManualAreaCmp.ts" />
