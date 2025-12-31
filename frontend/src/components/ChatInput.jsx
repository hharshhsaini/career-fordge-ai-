import { useState } from 'react';

export default function ChatInput({ onSubmit, isLoading }) {
  const [skills, setSkills] = useState('');
  const [interests, setInterests] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (skills.trim() && interests.trim()) {
      onSubmit(skills, interests);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-6 space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          What are your skills?
        </label>
        <textarea
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="e.g., Python, JavaScript, problem-solving, communication..."
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          rows={3}
          disabled={isLoading}
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          What are your interests?
        </label>
        <textarea
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          placeholder="e.g., AI, web development, data science, gaming..."
          className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
          rows={3}
          disabled={isLoading}
        />
      </div>
      <button
        type="submit"
        disabled={isLoading || !skills.trim() || !interests.trim()}
        className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Generating Your Career Path...' : 'Forge My Career Path 🚀'}
      </button>
    </form>
  );
}
