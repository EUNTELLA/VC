// Created: 2026-09-17 11:10:26
// To-do list app: add/edit/delete, completion toggle, category filter,
// and progress display. State is persisted to localStorage so it
// survives page reloads.

const STORAGE_KEY = "week04_todos";

const CATEGORY_LABELS = {
  work: "업무",
  personal: "개인",
  study: "공부",
};

let todos = loadTodos();
let currentFilter = "all";
let editingId = null;

const form = document.getElementById("todo-form");
const textInput = document.getElementById("todo-text");
const categorySelect = document.getElementById("todo-category");
const listEl = document.getElementById("todo-list");
const filtersEl = document.getElementById("filters");
const progressFillEl = document.getElementById("progress-fill");
const progressLabelEl = document.getElementById("progress-label");

function loadTodos() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function saveTodos() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

function addTodo(text, category) {
  todos.push({
    id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    text,
    category,
    completed: false,
    createdAt: Date.now(),
  });
  saveTodos();
  render();
}

function updateTodo(id, text, category) {
  const todo = todos.find((t) => t.id === id);
  if (!todo) return;
  todo.text = text;
  todo.category = category;
  saveTodos();
  render();
}

function deleteTodo(id) {
  todos = todos.filter((t) => t.id !== id);
  saveTodos();
  render();
}

function toggleComplete(id) {
  const todo = todos.find((t) => t.id === id);
  if (!todo) return;
  todo.completed = !todo.completed;
  saveTodos();
  render();
}

function createItemElement(todo) {
  const li = document.createElement("li");
  li.className = "todo-item" + (todo.completed ? " completed" : "");

  if (editingId === todo.id) {
    const input = document.createElement("input");
    input.type = "text";
    input.value = todo.text;

    const select = document.createElement("select");
    for (const [value, label] of Object.entries(CATEGORY_LABELS)) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      if (value === todo.category) option.selected = true;
      select.appendChild(option);
    }

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "저장";
    saveBtn.addEventListener("click", () => {
      const newText = input.value.trim();
      if (!newText) return;
      editingId = null;
      updateTodo(todo.id, newText, select.value);
    });

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "취소";
    cancelBtn.addEventListener("click", () => {
      editingId = null;
      render();
    });

    li.append(input, select, saveBtn, cancelBtn);
    return li;
  }

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.checked = todo.completed;
  checkbox.addEventListener("change", () => toggleComplete(todo.id));

  const text = document.createElement("span");
  text.className = "todo-text";
  text.textContent = todo.text;

  const tag = document.createElement("span");
  tag.className = `category-tag ${todo.category}`;
  tag.textContent = CATEGORY_LABELS[todo.category];

  const actions = document.createElement("span");
  actions.className = "todo-actions";

  const editBtn = document.createElement("button");
  editBtn.textContent = "수정";
  editBtn.addEventListener("click", () => {
    editingId = todo.id;
    render();
  });

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "삭제";
  deleteBtn.addEventListener("click", () => deleteTodo(todo.id));

  actions.append(editBtn, deleteBtn);
  li.append(checkbox, text, tag, actions);
  return li;
}

function render() {
  const visibleTodos =
    currentFilter === "all"
      ? todos
      : todos.filter((t) => t.category === currentFilter);

  listEl.innerHTML = "";
  if (visibleTodos.length === 0) {
    const empty = document.createElement("li");
    empty.className = "empty-state";
    empty.textContent = "할일이 없습니다.";
    listEl.appendChild(empty);
  } else {
    for (const todo of visibleTodos) {
      listEl.appendChild(createItemElement(todo));
    }
  }

  const total = todos.length;
  const done = todos.filter((t) => t.completed).length;
  const percent = total === 0 ? 0 : Math.round((done / total) * 100);
  progressFillEl.style.width = `${percent}%`;
  progressLabelEl.textContent = `${done} / ${total} 완료 (${percent}%)`;

  for (const btn of filtersEl.querySelectorAll(".filter-btn")) {
    btn.classList.toggle("active", btn.dataset.filter === currentFilter);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = textInput.value.trim();
  if (!text) return;
  addTodo(text, categorySelect.value);
  textInput.value = "";
  textInput.focus();
});

filtersEl.addEventListener("click", (event) => {
  const btn = event.target.closest(".filter-btn");
  if (!btn) return;
  currentFilter = btn.dataset.filter;
  render();
});

render();
