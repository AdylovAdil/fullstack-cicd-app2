import { useEffect, useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";
const STUDENT_NAME = import.meta.env.VITE_STUDENT_NAME || "Adil";
const STUDENT_ID = import.meta.env.VITE_STUDENT_ID || "YOUR_STUDENT_ID";

export default function App() {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const count = useMemo(() => items.length, [items]);

  async function loadItems() {
    try {
      setError("");
      const response = await fetch(`${API_URL}/api/data`);
      if (!response.ok) throw new Error("Не удалось загрузить данные");
      const data = await response.json();
      setItems(data);
    } catch (err) {
      setError(err.message || "Ошибка");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadItems();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    const value = title.trim();
    if (!value) return;

    try {
      setError("");
      const response = await fetch(`${API_URL}/api/data`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: value }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Ошибка при добавлении");

      setItems((prev) => [data, ...prev]);
      setTitle("");
    } catch (err) {
      setError(err.message || "Ошибка");
    }
  }

  async function handleDelete(id) {
    try {
      setError("");
      const response = await fetch(`${API_URL}/api/data/${id}`, {
        method: "DELETE",
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Ошибка при удалении");

      setItems((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(err.message || "Ошибка");
    }
  }

  return (
    <div className="page">
      <div className="container">
        <header className="hero">
          <div>
            <p className="badge">Full-Stack приложение с CI/CD</p>
            <h1>Трёхуровневое приложение: Frontend + Backend + PostgreSQL</h1>
            <p className="subtitle">
              React frontend получает данные из Flask API, а backend хранит их в базе данных.
            </p>
          </div>

          <div className="student-card">
            <span>Имя студента</span>
            <strong>{STUDENT_NAME}</strong>
            <span>ID студента</span>
            <strong>{STUDENT_ID}</strong>
          </div>
        </header>

        <section className="panel">
          <div className="panel-top">
            <div>
              <h2>Добавить запись</h2>
              <p>Проверь работу формы, API и базы данных.</p>
            </div>
            <div className="count">{count} записей</div>
          </div>

          <form className="form" onSubmit={handleSubmit}>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Введите задачу, item или запись"
            />
            <button type="submit">Добавить</button>
          </form>

          {error && <div className="error">{error}</div>}
        </section>

        <section className="panel">
          <div className="panel-top">
            <div>
              <h2>Список данных</h2>
              <p>Данные загружаются из API: {API_URL}</p>
            </div>
          </div>

          {loading ? (
            <div className="empty">Загрузка...</div>
          ) : items.length === 0 ? (
            <div className="empty">Пока нет записей. Добавь первую запись выше.</div>
          ) : (
            <ul className="list">
              {items.map((item) => (
                <li className="list-item" key={item.id}>
                  <div>
                    <div className="item-title">{item.title}</div>
                    <div className="item-meta">ID: {item.id}</div>
                  </div>
                  <button className="delete" onClick={() => handleDelete(item.id)}>
                    Удалить
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
