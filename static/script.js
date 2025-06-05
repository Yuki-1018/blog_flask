function showPost(id) {
  fetch(`/api/post/${id}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById('popup-title').innerText = data.title;
      document.getElementById('popup-body').innerText = data.content;
      document.getElementById('popup').classList.remove('hidden');
    });
}

function closePopup() {
  document.getElementById('popup').classList.add('hidden');
}
