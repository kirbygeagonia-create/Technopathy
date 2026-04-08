<template>
  <div class="search-bar" :class="{ 'is-expanded': isExpanded, 'has-results': showResults }">
    <div class="search-input-wrapper">
      <span class="material-icons search-icon">search</span>
      <input
        ref="inputRef"
        v-model="searchQuery"
        type="text"
        :placeholder="placeholder"
        class="search-input"
        @focus="onFocus"
        @blur="onBlur"
        @keyup.enter="onSearch"
        @input="onInput"
      />
      <button v-if="searchQuery" class="clear-btn" @click="clearSearch">
        <span class="material-icons">close</span>
      </button>
    </div>
    
    <!-- Search Results Dropdown -->
    <Transition name="slide-down">
      <div v-if="showResults && filteredResults.length > 0" class="search-results">
        <div
          v-for="result in filteredResults"
          :key="result.id || result.name"
          class="search-result-item"
          @click="selectResult(result)"
        >
          <span class="material-icons result-icon">{{ getIcon(result.type) }}</span>
          <div class="result-info">
            <span class="result-name">{{ result.name }}</span>
            <span class="result-type">{{ result.type }}</span>
          </div>
        </div>
      </div>
    </Transition>
    
    <!-- No Results -->
    <div v-else-if="showResults && searchQuery && filteredResults.length === 0" class="search-results empty">
      <span class="material-icons">search_off</span>
      <p>No results found for "{{ searchQuery }}"</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  placeholder: { type: String, default: 'Search...' },
  results: { type: Array, default: () => [] },
  maxResults: { type: Number, default: 8 },
  debounceMs: { type: Number, default: 200 }
})

const emit = defineEmits(['search', 'select', 'input'])

const searchQuery = ref('')
const isExpanded = ref(false)
const showResults = ref(false)
const inputRef = ref(null)
let debounceTimer = null

const filteredResults = computed(() => {
  if (!searchQuery.value) return []
  const query = searchQuery.value.toLowerCase()
  return props.results
    .filter(r => r.name?.toLowerCase().includes(query))
    .slice(0, props.maxResults)
})

function onInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('input', searchQuery.value)
    showResults.value = true
  }, props.debounceMs)
}

function onSearch() {
  emit('search', searchQuery.value)
  showResults.value = true
}

function selectResult(result) {
  emit('select', result)
  searchQuery.value = result.name
  showResults.value = false
}

function clearSearch() {
  searchQuery.value = ''
  showResults.value = false
  inputRef.value?.focus()
}

function onFocus() {
  isExpanded.value = true
  if (searchQuery.value) showResults.value = true
}

function onBlur() {
  // Delay hiding results to allow click events
  setTimeout(() => {
    isExpanded.value = false
    showResults.value = false
  }, 200)
}

function getIcon(type) {
  switch (type?.toLowerCase()) {
    case 'facility': return 'apartment'
    case 'room': return 'meeting_room'
    case 'office': return 'business'
    case 'classroom': return 'school'
    case 'lab': return 'science'
    default: return 'place'
  }
}

// Expose methods for parent
defineExpose({
  focus: () => inputRef.value?.focus(),
  clear: clearSearch,
  setQuery: (q) => { searchQuery.value = q }
})
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  background: var(--color-surface, white);
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-full, 9999px);
  padding: 0 8px;
  transition: all 0.2s ease;
}

.search-input-wrapper:focus-within {
  border-color: var(--color-primary, #FF9800);
  box-shadow: 0 0 0 3px rgba(255, 152, 0, 0.1);
}

.search-icon {
  color: var(--color-text-hint, #999);
  font-size: 20px;
  margin: 0 8px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 8px;
  font-size: var(--text-base, 14px);
  font-family: var(--font-primary, inherit);
  color: var(--color-text-primary, #1a1a1a);
  outline: none;
}

.search-input::placeholder {
  color: var(--color-text-hint, #999);
}

.clear-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: var(--color-border, #eee);
  color: var(--color-text-secondary, #666);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: 4px;
}

.clear-btn:hover {
  background: var(--color-danger, #F44336);
  color: white;
}

.clear-btn .material-icons {
  font-size: 16px;
}

/* Search Results Dropdown */
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 8px;
  background: var(--color-surface, white);
  border: 1px solid var(--color-border, #ddd);
  border-radius: var(--radius-lg, 12px);
  box-shadow: var(--shadow-lg, 0 8px 32px rgba(0,0,0,0.15));
  max-height: 320px;
  overflow-y: auto;
  z-index: 100;
}

.search-results.empty {
  padding: 24px;
  text-align: center;
  color: var(--color-text-hint, #999);
}

.search-results.empty .material-icons {
  font-size: 48px;
  margin-bottom: 8px;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.search-result-item:first-child {
  border-radius: var(--radius-lg, 12px) var(--radius-lg, 12px) 0 0;
}

.search-result-item:last-child {
  border-radius: 0 0 var(--radius-lg, 12px) var(--radius-lg, 12px);
}

.search-result-item:hover {
  background: var(--color-bg, #f5f5f5);
}

.result-icon {
  color: var(--color-primary, #FF9800);
  font-size: 24px;
}

.result-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.result-name {
  font-size: var(--text-base, 14px);
  font-weight: 500;
  color: var(--color-text-primary, #1a1a1a);
}

.result-type {
  font-size: var(--text-xs, 12px);
  color: var(--color-text-secondary, #666);
  text-transform: capitalize;
}

/* Slide down transition */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
