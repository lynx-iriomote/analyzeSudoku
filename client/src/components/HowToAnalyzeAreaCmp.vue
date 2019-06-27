<template>
  <div class="how-to-area" id="howToArea">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      version="1.1"
      :viewBox="svgViebox"
      :width="svgWidth"
      :height="svgHeight"
    >
      <!-- 解析方法 -->
      <HowToAnalyzeCmp
        v-for="howTo in howToList"
        :key="howTo.id"
        :howTo="howTo"
        :msgSplit="msgSplit(howTo)"
        :startX="3"
        :startY="svgTextY(howTo)"
      />
    </svg>
  </div>
</template>

<style lang="scss" scoped>
.how-to-area {
  position: relative;
  padding: 0px;
  min-width: 300px;
  max-width: 450px;
  width: 450px;
  height: 160px;
  margin: auto;
  border: solid 1px $color-line;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>

<script lang="ts" src="@/components/ts/HowToAnalyzeAreaCmp.ts" />
