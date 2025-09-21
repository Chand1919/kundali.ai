// web/script.js
// Make sure you include jsPDF in your HTML before this script:
// <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("userForm");
  const modal = document.getElementById("errorModal");
  const errorMsg = document.getElementById("errorMsg");
  const closeBtn = document.getElementById("closeBtn");
  const resultCard = document.getElementById("result");

  // ===== Helper function to show error modal =====
  function showError(msg) {
    if (!modal) return alert(msg);
    errorMsg.textContent = msg;
    modal.style.display = "flex";
  }

  if (closeBtn) closeBtn.onclick = () => (modal.style.display = "none");

  // ===== Input formatting =====
  const aadhaarInput = document.getElementById("aadhaar");
  const panInput = document.getElementById("pan");

  aadhaarInput.addEventListener("input", () => {
    aadhaarInput.value = aadhaarInput.value.replace(/\D/g, "").slice(0, 12);
  });

  panInput.addEventListener("input", () => {
    panInput.value = panInput.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 10);
  });

  // ===== Form submission =====
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const payload = {
      name: document.getElementById("name").value.trim(),
      age: Number(document.getElementById("age").value),
      dob: document.getElementById("dob").value,
      aadhaar: aadhaarInput.value.trim(),
      pan: panInput.value.trim(),
      ration: document.getElementById("ration").value.trim(),
      declared_assets: Number(document.getElementById("declared_assets").value || 0),
    };

    // ===== Client-side validation =====
    if (!payload.name || payload.name.length < 3)
      return showError("Name must be at least 3 characters.");
    if (!payload.dob) return showError("Date of Birth is required.");
    if (!/^\d{12}$/.test(payload.aadhaar))
      return showError("Aadhaar must be exactly 12 digits.");
    if (!/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(payload.pan))
      return showError("PAN must be in format ABCDE1234F.");

    try {
      // ===== Mock assessment =====
      const assessment = {
        eligibility: payload.age >= 18 ? "eligible" : "not eligible",
        score: Math.floor(Math.random() * 100),
        assets_est: payload.declared_assets + 50000,
        note: "This is a mock assessment for demo purposes.",
      };

      // ===== Display Result =====
      resultCard.style.display = "block";
      resultCard.innerHTML = `
        <div style="padding:12px">
          <strong>Eligibility:</strong> ${assessment.eligibility.toUpperCase()}<br/>
          <strong>Score:</strong> ${assessment.score}<br/>
          <strong>Estimated assets (INR):</strong> ${assessment.assets_est}<br/>
          <p style="margin-top:8px;color:#374151">${assessment.note}</p>
          <button id="downloadPdfBtn" style="margin-top:8px;padding:6px 12px;">Download PDF</button>
        </div>
      `;

      // ===== Generate PDF =====
      const downloadBtn = document.getElementById("downloadPdfBtn");
      downloadBtn.onclick = () => {
        if (!window.jspdf) return showError("jsPDF library not loaded!");
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.setFontSize(16);
        doc.text("Eligibility Report", 20, 20);
        doc.setFontSize(12);
        doc.text(`Name: ${payload.name}`, 20, 40);
        doc.text(`Age: ${payload.age}`, 20, 50);
        doc.text(`DOB: ${payload.dob}`, 20, 60);
        doc.text(`Aadhaar: ${payload.aadhaar}`, 20, 70);
        doc.text(`PAN: ${payload.pan}`, 20, 80);
        doc.text(`Ration Card: ${payload.ration || "N/A"}`, 20, 90);
        doc.text(`Declared Assets: ₹${payload.declared_assets}`, 20, 100);
        doc.text(`Eligibility: ${assessment.eligibility.toUpperCase()}`, 20, 120);
        doc.text(`Score: ${assessment.score}`, 20, 130);
        doc.text(`Estimated Assets (INR): ${assessment.assets_est}`, 20, 140);
        doc.text(`Note: ${assessment.note}`, 20, 160);

        // ✅ Trigger download
        doc.save("eligibility_report.pdf");
      };

      form.reset();
    } catch (err) {
      console.error(err);
      showError("An unexpected error occurred.");
    }
  });
});
