// ───────── Selectors ─────────
const themeBubble   = document.querySelector('.theme-bubble');
const themeToggle   = document.querySelector('.theme-toggle');
const toDoInput     = document.querySelector('.todo-input');
const toDoBtn       = document.querySelector('.todo-btn');
const toDoList      = document.querySelector('.todo-list');
const standardTheme = document.querySelector('.standard-theme');
const lightTheme    = document.querySelector('.light-theme');
const darkerTheme   = document.querySelector('.darker-theme');
const forestTheme   = document.querySelector('.forest-theme');
const sunsetTheme   = document.querySelector('.sunset-theme');

// ───────── Event Listeners ─────────
// To‑Do actions
toDoBtn.addEventListener('click', addToDo);
toDoList.addEventListener('click', deletecheck);
document.addEventListener('DOMContentLoaded', getTodos);

// Theme actions
standardTheme.addEventListener('click', () => changeTheme('standard'));
lightTheme.addEventListener('click',    () => changeTheme('light'));
darkerTheme.addEventListener('click',   () => changeTheme('darker'));
forestTheme.addEventListener('click',   () => changeTheme('forest'));
sunsetTheme.addEventListener('click',   () => changeTheme('sunset'));

// Bubble toggle & click‑away
themeToggle.addEventListener('click', () => themeBubble.classList.toggle('open'));
themeBubble.addEventListener('click', e => e.stopPropagation());
document.addEventListener('click',    () => themeBubble.classList.remove('open'));

// ───────── Initialize saved theme ─────────
let savedTheme = localStorage.getItem('savedTheme');
if (!savedTheme) {
  changeTheme('standard');
} else {
  changeTheme(savedTheme);
}

// ───────── Functions ─────────

/**
 * POST new to‑do to server, then render it.
 */
async function addToDo(event) {
  event.preventDefault();

  const text = toDoInput.value.trim();
  if (!text) return alert("You must write something!");

  const res = await fetch('/api/todos', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ text })
  });
  if (!res.ok) {
    return alert("Failed to save task on server");
  }

  const todo = await res.json();
  renderTodo(todo);
  toDoInput.value = '';
}

/**
 * Handle click on check/delete buttons with server sync
 */
function deletecheck(event) {
  const btn = event.target.closest('button');
  if (!btn) return;

  const div = btn.parentElement;
  const id  = div.dataset.id;

  if (btn.classList.contains('delete-btn')) {
    fetch(`/api/todos/${id}`, { method: 'DELETE' })
      .then(res => {
        if (!res.ok) throw new Error();
        div.classList.add('fall');
        div.addEventListener('transitionend', () => div.remove());
      })
      .catch(_ => alert("Could not delete task"));
  }

  if (btn.classList.contains('check-btn')) {
    fetch(`/api/todos/${id}`, {
      method: 'PATCH',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({completed: !div.classList.contains('completed')})
    })
    .then(res => {
      if (!res.ok) throw new Error();
      div.classList.toggle('completed');
    })
    .catch(_ => alert("Could not update task"));
  }
}

/**
 * GET todos and render with completion status
 */
async function getTodos() {
  const res = await fetch('/api/todos');
  if (!res.ok) return console.error("Failed to load tasks");
  const todos = await res.json();
  todos.forEach(todo => {
    renderTodo(todo);
    if (todo.completed) {
      const div = document.querySelector(`[data-id="${todo.id}"]`);
      div.classList.add('completed');
    }
  });
}

/**
 * Render one to‑do item with timestamp
 */
function renderTodo(todo) {
  const toDoDiv = document.createElement('div');
  toDoDiv.classList.add('todo', `${savedTheme}-todo`);
  toDoDiv.dataset.id = todo.id;

  const li = document.createElement('li');
  li.classList.add('todo-item');
  
  // Create text node with timestamp
  const timeSpan = document.createElement('span');
  timeSpan.classList.add('todo-time');
  timeSpan.textContent = new Date(todo.created_at).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  li.textContent = todo.text;
  li.appendChild(timeSpan);
  toDoDiv.appendChild(li);

  const checkBtn = document.createElement('button');
  checkBtn.innerHTML = '<i class="fas fa-check"></i>';
  checkBtn.classList.add('check-btn', `${savedTheme}-button`);
  toDoDiv.appendChild(checkBtn);

  const delBtn = document.createElement('button');
  delBtn.innerHTML = '<i class="fas fa-trash"></i>';
  delBtn.classList.add('delete-btn', `${savedTheme}-button`);
  toDoDiv.appendChild(delBtn);

  toDoList.appendChild(toDoDiv);
}

/**
 * Theme management
 */
function changeTheme(color) {
  localStorage.setItem('savedTheme', color);
  savedTheme = color;

  document.body.className = color;
  if (color === 'darker') {
    document.getElementById('title').classList.add('darker-title');
  } else {
    document.getElementById('title').classList.remove('darker-title');
  }

  // Update inputs
  document.querySelector('input').className = `${color}-input`;

  // Update existing todos
  document.querySelectorAll('.todo').forEach(todo => {
    const isDone = todo.classList.contains('completed');
    todo.className = isDone
      ? `todo ${color}-todo completed`
      : `todo ${color}-todo`;
  });

  // Update buttons
  document.querySelectorAll('button').forEach(btn => {
    if (btn.classList.contains('check-btn')) {
      btn.className = `check-btn ${color}-button`;
    } else if (btn.classList.contains('delete-btn')) {
      btn.className = `delete-btn ${color}-button`;
    } else if (btn.classList.contains('todo-btn')) {
      btn.className = `todo-btn ${color}-button`;
    }
  });
}