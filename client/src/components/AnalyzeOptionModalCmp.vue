<template>
  <transition name="modal" appear>
    <div class="modal modal-overlay" @click.self="closeModal">
      <div class="modal-window">
        <!-- 行 -->
        <div class="modal-content">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            version="1.1"
            :viewBox="svgVieboxForRow"
            :width="svgWidthForRow"
            :height="svgHeightForRow"
          >
            <AnalyzeOptionRowCmp
              v-for="(analyzeOption, idx) in analyzeOptionList"
              :key="analyzeOption.id"
              :analyzeOption="analyzeOption"
              :startX="0"
              :startY="idx * svgHeightForRowPerOne"
              @check="check"
            />
          </svg>
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
// .input-add {
//   width: 100%;
//   height: 100%;
//   font-size: 150%;
// }
// .input-add::-webkit-input-placeholder {
//   color: $color-text-placeholder;
// }

// .input-add::-moz-placeholder {
//   color: $color-text-placeholder;
// }

// .input-add:-ms-input-placeholder {
//   color: $color-text-placeholder;
// }

// .icon-default {
//   fill: $color-icon-default;
// }

// .icon-checkbox-default {
//   fill: none;
//   stroke: white;
// }
// .icon-checkbox-flame {
//   fill: none;
//   stroke: white;
// }

.modal {
  &.modal-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    z-index: 30;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: $color-modal-overlay-background;
  }

  &-window {
    background: $color-background;
    border-radius: 15px;
    border: 2px solid $color-line;
    overflow: hidden;
  }

  &-content {
    padding: 10px;
    min-width: 400px;
    max-width: 500px;
    height: auto;
    min-height: 200px;
    max-height: 500px;
    margin: auto;
    overflow: auto;
    overflow-x: hidden;
  }
}

// オーバーレイのトランジション
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.4s;

  // オーバーレイに包含されているモーダルウィンドウのトランジション
  .modal-window {
    transition: opacity 0.4s, transform 0.4s;
  }
}

// ディレイを付けるとモーダルウィンドウが消えた後にオーバーレイが消える
.modal-leave-active {
  transition: opacity 0.6s ease 0.4s;
}

.modal-enter,
.modal-leave-to {
  opacity: 0;

  .modal-window {
    opacity: 0;
    transform: translateY(-20px);
  }
}
</style>

<script lang="ts" src="@/components/ts/AnalyzeOptionModalCmp.ts" />
