import TodoItem from './TodoItem';

export default function TodoList({ tasks, onToggle, onDelete, onEdit }) {
  if (!tasks.length) {
    return (
      <div className="empty-state">
        <p>No tasks yet. Add one to get started!</p>
      </div>
    );
  }
  return (
    <div className="task-list">
      {tasks.map(task => (
        <TodoItem
          key={task.id}
          task={task}
          onToggle={() => onToggle(task.id, task.completed)}
          onDelete={() => onDelete(task.id)}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}
