<template>
  <div id="app">
    <!-- TODO: ここらへんにサイドメニュー的なものを書く？ -->
    <div tabindex="0" id="mainContents">
      <router-view />
    </div>
  </div>
</template>

<style lang="scss">
body {
  background-color: $color-background;
  margin: 0;
}
#mainContents {
  outline: none;
}
</style>
