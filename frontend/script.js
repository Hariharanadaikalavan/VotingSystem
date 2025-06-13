fetch('http://localhost:5000/candidates')
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById('candidates');
    data.forEach(candidate => {
      const btn = document.createElement('button');
      btn.textContent = `${candidate.name} (${candidate.votes} votes)`;
      btn.onclick = () => vote(candidate.id);
      container.appendChild(btn);
    });
  });

function vote(candidateId) {
  const userId = localStorage.getItem("userId");
  const hasVoted = localStorage.getItem("hasVoted");

  if (!userId) {
    alert("Please login first.");
    window.location.href = "login.html";
    return;
  }

  if (hasVoted === "true") {
    alert("You have already voted!");
    return;
  }

  fetch('http://localhost:5000/vote', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ candidate_id: candidateId, user_id: userId })
  })
  .then(res => res.json())
  .then(msg => {
    alert(msg.message || msg.error);
    if (msg.message) {
      localStorage.setItem("hasVoted", "true");
      location.reload();
    }
  });
}
