// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  base: '/static/', // Make Vite build assets relative to Django's static path
  build: {
    outDir: '../recommender/static', // Build output goes to Django's static folder
    emptyOutDir: true, // Clean before each build
  },
});