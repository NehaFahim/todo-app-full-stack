"use client";
import { useState, useEffect } from 'react';

interface Todo {
  id?: number;
  title: string;
  is_completed: boolean;
}

export default function TodoApp() {
  const [tasks, setTasks] = useState<Todo[]>([]);
  const [newTitle, setNewTitle] = useState("");

  // API se tasks mangwana
  const fetchTasks = async () => {
    const res = await fetch('http://localhost:8000/tasks');
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => { fetchTasks(); }, []);

  // Task add karna
  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle) return;
    await fetch('http://localhost:8000/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newTitle }),
    });
    setNewTitle("");
    fetchTasks();
  };

  // Task status update karna
  const toggleComplete = async (id: number, currentStatus: boolean) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_completed: !currentStatus }),
    });
    fetchTasks();
  };

  const [chatInput, setChatInput] = useState("");
const [chatLog, setChatLog] = useState<{user: string, ai: string}[]>([]);

const handleChat = async () => {
  const res = await fetch(`http://localhost:8000/chat?prompt=${chatInput}`, { method: 'POST' });
  const data = await res.json();
  setChatLog([...chatLog, { user: chatInput, ai: data.reply }]);
  setChatInput("");
  fetchTasks(); // Task list refresh karein
};

  return (
    <main className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h1 className="text-2xl font-bold mb-4 text-center">Evolution of Todo</h1>
      
      <form onSubmit={addTask} className="flex gap-2 mb-6">
        <input 
          type="text" 
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="border p-2 grow rounded text-black"
        />
        <button className="bg-blue-500 text-white px-4 py-2 rounded">Add</button>
      </form>

      <ul className="space-y-3">
        {tasks.map((task) => (
          <li key={task.id} className="flex items-center justify-between border-b pb-2">
            <span className={task.is_completed ? "line-through text-gray-400" : "text-black"}>
              {task.title}
            </span>
            <input 
              type="checkbox" 
              checked={task.is_completed} 
              onChange={() => toggleComplete(task.id!, task.is_completed)}
              className="w-5 h-5 cursor-pointer"
            />
          </li>
        ))}
      </ul>
      <div className="mt-10 border-t pt-5">
  <h2 className="text-xl font-bold mb-3">AI Assistant</h2>
  <div className="bg-gray-100 p-3 h-40 overflow-y-auto mb-2 text-black text-sm">
    {chatLog.map((log, i) => (
      <div key={i} className="mb-2">
        <b>You:</b> {log.user} <br/>
        <b>AI:</b> {log.ai}
      </div>
    ))}
  </div>
  <div className="flex gap-2">
    <input 
      value={chatInput} 
      onChange={(e) => setChatInput(e.target.value)} 
      className="border p-2 grow text-black" 
      placeholder="Ask AI (e.g. 'Add milk to list')"
    />
    <button onClick={handleChat} className="bg-green-500 text-white px-4 py-2 rounded">Send</button>
  </div>
</div>
    </main>
  );
}