<!-- frontend/src/App.vue -->
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Disease {
  id: number
  name: string
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const diseases = ref<Disease[]>([])
const explored = ref<string[]>([])

const screen = ref<'spinner' | 'history'>('spinner')
const selectedDisease = ref<string | null>(null)
const spinning = ref(false)
const loading = ref(true)
const error = ref<string | null>(null)
const rotation = ref(0)

const unexplored = computed(() =>
  diseases.value.filter(d => !explored.value.includes(d.name))
)

const progress = computed(() =>
  diseases.value.length
    ? Math.round((explored.value.length / diseases.value.length) * 100)
    : 0
)

// Load diseases and history from FastAPI
async function loadData() {
  loading.value = true
  error.value = null

  try {
    const [diseasesResponse, exploredResponse] = await Promise.all([
      fetch(`${API_URL}/diseases`),
      fetch(`${API_URL}/explored`)
    ])

    if (!diseasesResponse.ok || !exploredResponse.ok) {
      throw new Error('Failed to load application data.')
    }

    diseases.value = await diseasesResponse.json()

    const history = await exploredResponse.json()
    explored.value = history.map((item: { name: string }) => item.name)
  } catch (err) {
    error.value = 'Cannot connect to the backend. Make sure FastAPI is running.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

async function spin() {
  if (spinning.value || unexplored.value.length === 0) return

  spinning.value = true
  error.value = null

  const index = Math.floor(Math.random() * unexplored.value.length)
  const disease = unexplored.value[index]

  rotation.value += 1800 + Math.random() * 1800

  // Wait for the spinner animation
  await new Promise(resolve => setTimeout(resolve, 3500))

  try {
    // Save exploration in Supabase through FastAPI
    const response = await fetch(`${API_URL}/explored/${disease.id}`, {
      method: 'POST'
    })

    if (!response.ok) {
      throw new Error('Failed to save explored disease.')
    }

    selectedDisease.value = disease.name

    if (!explored.value.includes(disease.name)) {
      explored.value.push(disease.name)
    }
  } catch (err) {
    error.value = 'Could not save your exploration. Please try again.'
    console.error(err)
  } finally {
    spinning.value = false
  }
}

async function resetProgress() {
  if (!confirm('Reset all explored diseases?')) return

  error.value = null

  try {
    const response = await fetch(`${API_URL}/explored`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('Failed to reset progress.')
    }

    explored.value = []
    selectedDisease.value = null
  } catch (err) {
    error.value = 'Could not reset progress.'
    console.error(err)
  }
}
</script>

<template>
  <div class="app">
    <header>
      <h1>MedSpin</h1>

      <nav>
        <button
          :class="{ active: screen === 'spinner' }"
          @click="screen = 'spinner'"
        >
          Spinner
        </button>

        <button
          :class="{ active: screen === 'history' }"
          @click="screen = 'history'"
        >
          History
        </button>
      </nav>
    </header>

    <main>
      <p v-if="error" class="error">{{ error }}</p>

      <p v-if="loading" class="subtitle">Loading diseases...</p>

      <!-- SPINNER SCREEN -->
      <section v-else-if="screen === 'spinner'" class="spinner-screen">
        <p class="subtitle">Your next medical learning challenge</p>

        <div class="wheel-container">
          <div class="pointer"></div>

          <div
            class="wheel"
            :class="{ spinning }"
            :style="{ transform: `rotate(${rotation}deg)` }"
          >
            <span>DISEASE</span>
          </div>
        </div>

        <button
          class="spin-button"
          :disabled="spinning || unexplored.length === 0"
          @click="spin"
        >
          {{
            spinning
              ? 'Spinning...'
              : unexplored.length === 0
                ? 'All diseases explored'
                : 'SPIN'
          }}
        </button>

        <div v-if="selectedDisease && !spinning" class="result">
          <p>Your next disease</p>
          <h2>{{ selectedDisease }}</h2>
        </div>

        <div class="stats">
          <span>{{ unexplored.length }} remaining</span>
          <span>{{ explored.length }} explored</span>
          <span>{{ progress }}% complete</span>
        </div>

        <div class="progress">
          <div :style="{ width: progress + '%' }"></div>
        </div>
      </section>

      <!-- HISTORY SCREEN -->
      <section v-else class="history-screen">
        <h2>Explored Diseases</h2>

        <p class="subtitle">
          {{ explored.length }} / {{ diseases.length }} diseases
        </p>

        <div v-if="explored.length" class="history-list">
          <div
            v-for="(disease, index) in explored"
            :key="disease"
            class="history-item"
          >
            <span>{{ index + 1 }}</span>
            <span>{{ disease }}</span>
          </div>
        </div>

        <p v-else class="empty">
          No diseases explored yet. Start spinning!
        </p>

        <button
          v-if="explored.length"
          class="reset-button"
          @click="resetProgress"
        >
          Reset Progress
        </button>
      </section>
    </main>
  </div>
</template>
