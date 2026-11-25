const oneDayCheckbox = document.getElementById("oneDay");
const startDateInput = document.getElementById("startDate");
const endDateInput = document.getElementById("endDate");

let fp = null;

function initRangePicker() {
  if (fp) fp.destroy();

  endDateInput.disabled = false;

  fp = flatpickr(startDateInput, {
    dateFormat: "Y-m-d",
    mode: "range",
    minDate: "today",
    plugins: [new rangePlugin({ input: "#endDate" })],
    onChange: (selectedDates) => {
      // selectedDates will be [start] or [start, end]
      if (oneDayCheckbox.checked && selectedDates[0]) {
        // if someone toggles checkbox later, keep sync safe
        const d = fp.formatDate(selectedDates[0], "Y-m-d");
        endDateInput.value = d;
      }
    },
  });
}

/**
 * Create Flatpickr in "single" mode for one-day visit
 * and always mirror start -> end.
 */
function initSinglePicker() {
  if (fp) fp.destroy();

  endDateInput.disabled = true;

  fp = flatpickr(startDateInput, {
    dateFormat: "Y-m-d",
    minDate: "today",
    mode: "single",
    onChange: (selectedDates) => {
      if (selectedDates[0]) {
        const d = fp.formatDate(selectedDates[0], "Y-m-d");
        endDateInput.value = d; // mirror
      } else {
        endDateInput.value = "";
      }
    },
  });

  // If there is already a start date, mirror it immediately
  if (startDateInput.value) endDateInput.value = startDateInput.value;
}

/* ---------- Toggle one-day logic ---------- */
oneDayCheckbox.addEventListener("change", () => {
  if (oneDayCheckbox.checked) {
    // switch to single picker + mirror end date
    initSinglePicker();
  } else {
    // switch back to range picker
    // keep current start date, but clear end date if it was mirrored
    const keepStart = startDateInput.value || "";
    initRangePicker();
    if (keepStart) startDateInput.value = keepStart;
  }
});

/* ---------- Submit booking ---------- */
function submitHomepage() {
  const oneDay = oneDayCheckbox.checked;
  const startDate = (startDateInput.value || "").trim();
  const endDate = (oneDay ? startDate : (endDateInput.value || "").trim());
  const guests = (document.getElementById("guests").value || "").trim();
  const park = (document.getElementById("park").value || "").trim();
  const error = document.getElementById("error");

  error.classList.add("hidden");
  error.textContent = "";

  if (!startDate) {
    error.textContent = "Please select a start date.";
    error.classList.remove("hidden");
    return;
  }

  if (!oneDay && !endDate) {
    error.textContent = "Please select an end date.";
    error.classList.remove("hidden");
    return;
  }

  if (!guests || Number(guests) < 1) {
    error.textContent = "Please enter a valid number of guests.";
    error.classList.remove("hidden");
    return;
  }

  if (!park) {
    error.textContent = "Please select a park location.";
    error.classList.remove("hidden");
    return;
  }

  // Call the CUSTOMER WEBSITE backend (stores session + returns correct nextUrl)
  fetch("/homepage/submit", {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ oneDay, startDate, endDate, guests, park }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data.success) {
        error.textContent = data.message || "Submit failed.";
        error.classList.remove("hidden");
        return;
      }
      window.location.href = data.nextUrl; // "/payments/pay" or "/booking/"
    })
    .catch(() => {
      error.textContent = "Something went wrong. Please try again.";
      error.classList.remove("hidden");
    });
}

/* ---------- Init on load ---------- */
initRangePicker();
