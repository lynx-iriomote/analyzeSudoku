<template>
  <div>
    <AnalyzeHistoryManualAreaCmp />
    <v-touch
      @swipeleft="moveNextHistory"
      @swiperight="moveBackHistory"
      :swipe-options="{ direction: 'horizontal' }"
    >
      <FlameCmp :flame="flame" />
    </v-touch>
    <HowToAnalyzeAreaCmp
      :howToList="howToList"
      :hilightHowToIdx="hilightHowToIdx"
    />
    <PagingAreaCmp />
    <MsgAreaCmp v-show="isMsgArea" />
  </div>
</template>

<style lang="scss">
</style>

<script lang="ts" src="@/views/ts/AnalyzeHistoryPage.ts" />
