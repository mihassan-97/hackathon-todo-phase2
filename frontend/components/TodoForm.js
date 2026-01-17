export default function TodoForm({ title, setTitle, handleAddTask, loading }) {
  return (
    <form onSubmit={handleAddTask} className="form">
      <input
        type="text"
        value={title}
        onChange={e => setTitle(e.target.value)}
        placeholder="Add a new task..."
        className="input"
        disabled={loading}
      />
      <button type="submit" className="btn btn-add" disabled={loading}>
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
