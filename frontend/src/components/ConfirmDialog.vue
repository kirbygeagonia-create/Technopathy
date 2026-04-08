<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="visible" class="confirm-dialog-overlay" @click="onCancel">
        <div class="confirm-dialog" @click.stop>
          <div class="confirm-dialog-header">
            <span v-if="icon" class="material-icons confirm-dialog-icon" :class="type">{{ icon }}</span>
            <h3>{{ title }}</h3>
          </div>
          <p class="confirm-dialog-message">{{ message }}</p>
          <div class="confirm-dialog-actions">
            <button class="btn-secondary" @click="onCancel">{{ cancelText }}</button>
            <button class="btn-primary" :class="type" @click="onConfirm">{{ confirmText }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: Boolean,
  title: { type: String, default: 'Confirm' },
  message: { type: String, required: true },
  type: { type: String, default: 'danger' }, // danger, warning, info
  confirmText: { type: String, default: 'Confirm' },
  cancelText: { type: String, default: 'Cancel' }
})

const emit = defineEmits(['confirm', 'cancel'])

const icon = computed(() => {
  switch (props.type) {
    case 'danger': return 'delete_forever'
    case 'warning': return 'warning'
    case 'info': return 'info'
    default: return 'help'
  }
})

function onConfirm() {
  emit('confirm')
}

function onCancel() {
  emit('cancel')
}
</script>

<style scoped>
.confirm-dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 16px;
}

.confirm-dialog {
  background: var(--color-surface, white);
  border-radius: var(--radius-lg, 12px);
  padding: 24px;
  max-width: 400px;
  width: 100%;
  box-shadow: var(--shadow-lg, 0 8px 32px rgba(0,0,0,0.2));
}

.confirm-dialog-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.confirm-dialog-header h3 {
  font-size: var(--text-lg, 18px);
  font-weight: 600;
  color: var(--color-text-primary, #1a1a1a);
  margin: 0;
}

.confirm-dialog-icon {
  font-size: 28px;
}

.confirm-dialog-icon.danger { color: var(--color-danger, #F44336); }
.confirm-dialog-icon.warning { color: var(--color-warning, #FF9800); }
.confirm-dialog-icon.info { color: var(--color-info, #2196F3); }

.confirm-dialog-message {
  font-size: var(--text-base, 14px);
  color: var(--color-text-secondary, #666);
  margin-bottom: 24px;
  line-height: 1.5;
}

.confirm-dialog-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 10px 20px;
  background: var(--color-bg, #f5f5f5);
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-md, 8px);
  color: var(--color-text-primary, #1a1a1a);
  font-family: var(--font-primary, inherit);
  font-size: var(--text-sm, 14px);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--color-surface, white);
}

.btn-primary {
  padding: 10px 20px;
  background: var(--color-primary, #FF9800);
  border: none;
  border-radius: var(--radius-md, 8px);
  color: white;
  font-family: var(--font-primary, inherit);
  font-size: var(--text-sm, 14px);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-primary.danger {
  background: var(--color-danger, #F44336);
}

.btn-primary.warning {
  background: var(--color-warning, #FF9800);
}

.btn-primary.info {
  background: var(--color-info, #2196F3);
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
