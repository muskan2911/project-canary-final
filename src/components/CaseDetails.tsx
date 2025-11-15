import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Case } from '../types/case';

export default function CaseDetails() {
  const { caseId } = useParams();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState<Partial<Case>>({});
  const [comments, setComments] = useState<string[]>([]);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    fetch(`/api/cases/${caseId}`)
      .then(res => res.json())
      .then(data => {
        setCaseData(data);
        setForm(data);
        // Split comments by newline for display
        setComments(data.comments ? data.comments.split('\n') : []);
        setLoading(false);
      });
  }, [caseId]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    await fetch(`/api/cases/${caseId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    setEditMode(false);
    window.location.reload();
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    await fetch(`/api/cases/${caseId}/comment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment: newComment })
    });
    setNewComment('');
    // Reload case data to get updated comments
    const res = await fetch(`/api/cases/${caseId}`);
    const data = await res.json();
    setCaseData(data);
    setForm(data);
    setComments(data.comments ? data.comments.split('\n') : []);
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!caseData) return <div className="p-8 text-center">Case not found.</div>;

  return (
    <div className="max-w-2xl mx-auto p-8">
      <h2 className="text-2xl font-bold mb-4">Case Details: {caseData.case_id}</h2>
      <div className="space-y-4">
        <div>
          <label className="font-semibold">Customer:</label>
          {editMode ? (
            <input name="customer_name" value={form.customer_name || ''} onChange={handleChange} className="border p-1 ml-2" />
          ) : (
            <span className="ml-2">{caseData.customer_name}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Priority:</label>
          {editMode ? (
            <select name="priority" value={form.priority || ''} onChange={handleChange} className="border p-1 ml-2">
              <option>Low</option>
              <option>Medium</option>
              <option>High</option>
              <option>Critical</option>
            </select>
          ) : (
            <span className="ml-2">{caseData.priority}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Type:</label>
          {editMode ? (
            <select name="type" value={form.type || ''} onChange={handleChange} className="border p-1 ml-2">
              <option>Inquiry</option>
              <option>Incident</option>
              <option>Jira</option>
              <option>Bug</option>
              <option>Feature Request</option>
            </select>
          ) : (
            <span className="ml-2">{caseData.type}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Product:</label>
          {editMode ? (
            <input name="product" value={form.product || ''} onChange={handleChange} className="border p-1 ml-2" />
          ) : (
            <span className="ml-2">{caseData.product}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Status:</label>
          {editMode ? (
            <select name="status" value={form.status || ''} onChange={handleChange} className="border p-1 ml-2">
              <option>Open</option>
              <option>In Progress</option>
              <option>Resolved</option>
              <option>Closed</option>
            </select>
          ) : (
            <span className="ml-2">{caseData.status}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Description:</label>
          {editMode ? (
            <textarea name="description" value={form.description || ''} onChange={handleChange} className="border p-1 ml-2 w-full" />
          ) : (
            <span className="ml-2">{caseData.description}</span>
          )}
        </div>
        <div>
          <label className="font-semibold">Jira ID/URL:</label>
          {editMode ? (
            <input
              name="jira_id"
              value={form.jira_id || ''}
              onChange={handleChange}
              className="border p-1 ml-2 w-full"
              placeholder="Jira ID or full URL"
            />
          ) : (
            form.jira_id ? (
              <a
                href={form.jira_id.startsWith('http') ? form.jira_id : `https://jira.example.com/browse/${form.jira_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-2 text-blue-700 underline hover:text-blue-900"
              >
                {form.jira_id}
              </a>
            ) : (
              <span className="ml-2">-</span>
            )
          )}
        </div>
        <div>
          <label className="font-semibold">Snow ID/URL:</label>
          {editMode ? (
            <input
              name="snow_id"
              value={form.snow_id || ''}
              onChange={handleChange}
              className="border p-1 ml-2 w-full"
              placeholder="Snow ID or full URL"
            />
          ) : (
            form.snow_id ? (
              <a
                href={form.snow_id.startsWith('http') ? form.snow_id : `https://snow.example.com/incident/${form.snow_id}`}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-2 text-purple-700 underline hover:text-purple-900"
              >
                {form.snow_id}
              </a>
            ) : (
              <span className="ml-2">-</span>
            )
          )}
        </div>
        <div>
          <label className="font-semibold">Created:</label>
          <span className="ml-2">{caseData.created_date}</span>
        </div>
        <div>
          <label className="font-semibold">Geography:</label>
          <span className="ml-2">{caseData.geography || '-'}</span>
        </div>
        <div>
          <label className="font-semibold">Comments:</label>
          <ul className="ml-4 list-disc">
            {comments.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
          <div className="mt-2 flex">
            <input
              type="text"
              value={newComment}
              onChange={e => setNewComment(e.target.value)}
              className="border p-1 flex-1"
              placeholder="Add a comment..."
            />
            <button onClick={handleAddComment} className="ml-2 px-3 py-1 bg-blue-600 text-white rounded">Add</button>
          </div>
        </div>
        <div className="mt-4">
          {editMode ? (
            <button onClick={handleSave} className="px-4 py-2 bg-green-600 text-white rounded">Save</button>
          ) : (
            <button onClick={() => setEditMode(true)} className="px-4 py-2 bg-blue-600 text-white rounded">Edit</button>
          )}
        </div>
      </div>
    </div>
  );
}
