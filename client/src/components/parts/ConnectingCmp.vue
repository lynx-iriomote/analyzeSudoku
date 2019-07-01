<template>
  <div>
    <div class="loader">
      <span>C</span>
      <span>O</span>
      <span>N</span>
      <span>N</span>
      <span>E</span>
      <span>C</span>
      <span>T</span>
      <div class="covers">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.loader {
  position: relative;
  margin: auto;
  width: 200px;
  color: $color-text-connect;
  text-align: center;
}

.loader:after {
  content: "";
  display: table;
  clear: both;
}

span {
  float: left;
  width: calc(100% / 7);
  height: 100%;
  line-height: 100px;
}

.covers {
  position: absolute;
  height: 100%;
  width: 200px;
}

.covers span {
  background: rgba($color-background, 0.7);
  animation: up 3s infinite;
}

@keyframes up {
  0% {
    margin-bottom: 0;
  }
  16% {
    margin-bottom: 100%;
    height: 0px;
  }
  50% {
    margin-bottom: 0;
  }
  100% {
    margin-bottom: 0;
  }
}

.covers span:nth-child(2) {
  animation-delay: 0.142857s;
}
.covers span:nth-child(3) {
  animation-delay: 0.285714s;
}
.covers span:nth-child(4) {
  animation-delay: 0.428571s;
}
.covers span:nth-child(5) {
  animation-delay: 0.571428s;
}
.covers span:nth-child(6) {
  animation-delay: 0.714285s;
}
.covers span:nth-child(7) {
  animation-delay: 0.857142s;
}
</style>
