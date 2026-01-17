import { useState } from 'react';

export default function TodoItem({ task, onToggle, onDelete, onEdit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);

  const handleSaveEdit = () => {
    if (editTitle.trim()) {
      onEdit(task.id, editTitle);
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
            onChange={e => setEditTitle(e.target.value)}
            onBlur={handleSaveEdit}
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
