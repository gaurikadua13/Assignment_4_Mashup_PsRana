document.addEventListener("DOMContentLoaded", () => {
  const formEl = document.querySelector("form");
  const submitBtn = document.getElementById("submitBtn");
  const btnText = document.getElementById("btnText");
  const loader = document.getElementById("loader");
  
  loader.style.display = "none";

  formEl.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const singerVal = document.getElementById("singer").value.trim();
    const videosVal = document.getElementById("videos").value;
    const durationVal = document.getElementById("duration").value;
    const emailVal = document.getElementById("email").value.trim();

    if (!singerVal) {
      alert("Please enter a singer name");
      return;
    }
    if (isNaN(videosVal) || videosVal < 10) {
      alert("Videos must be 10 or more");
      return;
    }
    if (isNaN(durationVal) || durationVal < 20) {
      alert("Duration must be 20 seconds or more");
      return;
    }
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailVal || !emailPattern.test(emailVal)) {
      alert("Please enter a valid email address");
      return;
    }

    submitBtn.disabled = true;
    btnText.style.display = "none";
    loader.style.display = "block";

    async function pollStatus(taskId) {
      const response = await fetch(`/status/${taskId}`);
      const result = await response.json();
      return result.status;
    }

    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          singer: singerVal,
          videos: videosVal,
          duration: durationVal,
          email: emailVal
        })
      });

      if (!res.ok) {
        throw new Error("Request failed");
      }

      const data = await res.json();
      const taskId = data.job_id;
      
      const checkInterval = setInterval(async () => {
        const currentStatus = await pollStatus(taskId);
        
        if (currentStatus === "done") {
          clearInterval(checkInterval);
          loader.style.display = "none";
          btnText.style.display = "inline";
          submitBtn.disabled = false;
          alert("Mashup sent to your email successfully!");
        } else if (currentStatus === "error") {
          clearInterval(checkInterval);
          loader.style.display = "none";
          btnText.style.display = "inline";
          submitBtn.disabled = false;
          alert("Failed to create mashup. Please verify the singer name and try again.");
        }
      }, 5000);
      
    } catch (err) {
      loader.style.display = "none";
      btnText.style.display = "inline";
      submitBtn.disabled = false;
      alert("An error occurred. Please try again.");
      console.error(err);
    }
  });
});
