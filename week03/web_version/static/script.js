// Created: 2026-09-17 10:32:30
// Canvas drawing logic and prediction request for the digit recognizer.

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const resultEl = document.getElementById("result");

const BRUSH_WIDTH = 20;

let isDrawing = false;
let lastX = 0;
let lastY = 0;

function resetCanvas() {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "white";
  ctx.lineWidth = BRUSH_WIDTH;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
}

resetCanvas();

function getPointerPosition(event) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}

function startDrawing(event) {
  isDrawing = true;
  const { x, y } = getPointerPosition(event);
  lastX = x;
  lastY = y;
}

function draw(event) {
  if (!isDrawing) return;
  const { x, y } = getPointerPosition(event);
  ctx.beginPath();
  ctx.moveTo(lastX, lastY);
  ctx.lineTo(x, y);
  ctx.stroke();
  lastX = x;
  lastY = y;
}

function stopDrawing() {
  isDrawing = false;
}

canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("mousemove", draw);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

document.getElementById("clear-btn").addEventListener("click", () => {
  resetCanvas();
  resultEl.textContent = "Draw a digit (0-9)";
});

document.getElementById("predict-btn").addEventListener("click", async () => {
  const imageData = canvas.toDataURL("image/png");

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: imageData }),
  });

  const data = await response.json();

  if (data.error) {
    resultEl.textContent = data.error;
    return;
  }

  resultEl.textContent = `Predicted digit: ${data.digit}`;
});
