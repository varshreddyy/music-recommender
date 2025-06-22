import { defineConfig } from 'vite'

export default defineConfig({
  base: '/static/',
  build: {
    outDir: '../recommender/static',
    emptyOutDir: true,
  },
})