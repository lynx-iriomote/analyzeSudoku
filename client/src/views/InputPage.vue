<template>
  <div class="input-page">
    <InputPageManualAreaCmp />
    <FlameCmp :flame="flame" />
    <BtnAreaCmp />
    <SaveModalCmp v-if="isSaveModal" />
    <AnalyzeOptionModalCmp v-if="isAnalyzeOptionModal" />
    <MsgAreaCmp v-show="isMsgArea" />
    <ConnectingModalCmp v-if="isConnecting" />
  </div>
</template>

<style lang="scss" scoped>
.input-page {
  padding: 5px;
}
</style>

<script lang="ts" src="@/views/ts/InputPage.ts" />
