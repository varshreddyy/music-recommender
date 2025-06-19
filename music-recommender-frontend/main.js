async function getRecommendations() {
  const songInput = document.getElementById('song-name');
  const songName = songInput.value.trim();
  const errorMsg = document.getElementById('error-msg');
  const list = document.getElementById('recommendations');

  // Reset display
  errorMsg.textContent = '';
  list.innerHTML = '';

  if (!songName) {
    errorMsg.textContent = "Please enter a song name.";
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recommend/?song_name=${encodeURIComponent(songName)}`);
    
    if (!response.ok) {
      const data = await response.json();
      errorMsg.textContent = data.error || "An error occurred.";
      return;
    }

    const data = await response.json();

    if (data.length === 0) {
      errorMsg.textContent = "No recommendations found.";
      return;
    }

    // Populate recommendations
    data.forEach((song) => {
      const li = document.createElement('li');
      li.textContent = `${song.song} by ${song.artist}`;
      list.appendChild(li);
    });
  } catch (error) {
    console.error("Fetch error:", error);
    errorMsg.textContent = "Server error. Please try again later.";
  }
}

// Attach event listeners (this replaces onclick in HTML)
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('recommend-btn')?.addEventListener('click', getRecommendations);

  document.getElementById('song-name')?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      getRecommendations();
    }
  });
});