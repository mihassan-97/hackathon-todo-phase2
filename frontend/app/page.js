'use client';

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/page.css';

export default function Home() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Fetch all tasks
  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await axios.get(`${API_URL}/tasks`);
      setTasks(response.data);
    } catch (err) {
      setError('Failed to fetch tasks. Make sure backend is running at ' + API_URL);
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  // Add a new task
  const handleAddTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Task title cannot be empty');
      return;
    }

    try {
      setError('');
      const response = await axios.post(`${API_URL}/tasks`, { title });
      setTasks([...tasks, response.data]);
      setTitle('');
    } catch (err) {
      setError('Failed to create task');
      console.error('Add error:', err);
    }
  };

  // Toggle task completion status
  const handleToggleTask = async (taskId, currentStatus) => {
    try {
      setError('');
      const response = await axios.put(`${API_URL}/tasks/${taskId}`, {
        completed: !currentStatus,
      });
      setTasks(tasks.map((task) => (task.id === taskId ? response.data : task)));
    } catch (err) {
      setError('Failed to update task');
      console.error('Update error:', err);
    }
  };

  // Update task title
  const handleEditTask = async (taskId, newTitle) => {
    if (!newTitle.trim()) {
      setError('Task title cannot be empty');
      return;
    }

    try {
      setError('');
      const response = await axios.put(`${API_URL}/tasks/${taskId}`, {
        title: newTitle,
      });
      setTasks(tasks.map((task) => (task.id === taskId ? response.data : task)));
    } catch (err) {
      setError('Failed to update task title');
      console.error('Edit error:', err);
    }
  };

  // Delete a task
  const handleDeleteTask = async (taskId) => {
    try {
      setError('');
      await axios.delete(`${API_URL}/tasks/${taskId}`);
      setTasks(tasks.filter((task) => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Delete error:', err);
    }
  };

  return (
    <main className="container">
      <div className="app-wrapper">
        <h1>📝 My Tasks</h1>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleAddTask} className="form">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Add a new task..."
            className="input"
            disabled={loading}
          />
          <button type="submit" className="btn btn-add" disabled={loading}>
            {loading ? 'Adding...' : 'Add Task'}
          </button>
        </form>

        {loading && tasks.length === 0 ? (
          <div className="loading">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="empty-state">
            <p>No tasks yet. Add one to get started!</p>
          </div>
        ) : (
          <div className="task-list">
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggle={() => handleToggleTask(task.id, task.completed)}
                onDelete={() => handleDeleteTask(task.id)}
              />
            ))}
          </div>
        )}

        <div className="stats">
          <p>
            Total: <strong>{tasks.length}</strong> | Completed:{' '}
            <strong>{tasks.filter((t) => t.completed).length}</strong>
          </p>
        </div>
      </div>
    </main>
  );
}

function TaskItem({ task, onToggle, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);

  const handleSaveEdit = () => {
    if (editTitle.trim()) {
      onToggle.parent?.handleEditTask?.(task.id, editTitle);
      setIsEditing(false);
    }
  };

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      <div className="task-content">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={onToggle}
          className="checkbox"
        />
        {isEditing ? (
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            onBlur={() => setIsEditing(false)}
            className="task-edit-input"
            autoFocus
          />
        ) : (
          <span
            className="task-title"
            onDoubleClick={() => setIsEditing(true)}
            title="Double-click to edit"
          >
            {task.title}
          </span>
        )}
      </div>
      <button onClick={onDelete} className="btn btn-delete">
        🗑️
      </button>
    </div>
  );
}
