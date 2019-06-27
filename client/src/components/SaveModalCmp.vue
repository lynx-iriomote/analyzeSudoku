<template>
  <transition name="modal" appear>
    <div class="modal modal-overlay" @click.self="closeModal">
      <div class="modal-window">
        <div class="modal-header">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            version="1.1"
            viewBox="0 0 400 50"
            width="400"
            height="50"
          >
            <!-- 追加入力 -->
            <foreignObject width="350" height="50" x="0" y="0">
              <input
                xmlns="http://www.w3.org/1999/xhtml"
                type="text"
                placeholder="記録名(デフォルトで日時)"
                maxlength="20"
                class="input-add"
                v-model="saveName"
              />
            </foreignObject>

            <!-- 追加アイコン -->
            <use
              v-bind="{
                'xlink:href': require('@/assets/svg/plus.svg') + '#iconPlus'
              }"
              width="40"
              height="40"
              class="icon-default"
              x="355"
              y="5"
            />
            <rect
              width="40"
              height="40"
              x="355"
              y="5"
              fill="white"
              fill-opacity="0"
              @click.stop="add"
            />
          </svg>
        </div>

        <!-- 行 -->
        <div class="modal-content">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            version="1.1"
            :viewBox="svgVieboxForRow"
            :width="svgWidthForRow"
            :height="svgHeightForRow"
          >
            <SaveModalRowCmp
              v-for="(save, idx) in saveList"
              :key="save.id"
              :save="save"
              :startX="2"
              :startY="idx * svgHeightForRowPerOne"
              @clear-save="clearSave"
              @update-save="updateSave"
              @reflect-save="reflectSave"
            />
          </svg>
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="scss" scoped>
.input-add {
  width: 100%;
  height: 100%;
  font-size: 150%;
}
.input-add::-webkit-input-placeholder {
  color: $color-text-placeholder;
}

.input-add::-moz-placeholder {
  color: $color-text-placeholder;
}

.input-add:-ms-input-placeholder {
  color: $color-text-placeholder;
}

.icon-default {
  fill: $color-icon-default;
}

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

  &-header {
    padding-top: 10px;
    padding-left: 10px;
    padding-right: 10px;
    min-width: 400px;
    max-width: 500px;
    height: 50px;
    margin: auto;
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

<script lang="ts" src="@/components/ts/SaveModalCmp.ts" />
