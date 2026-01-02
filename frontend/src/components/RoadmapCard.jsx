import { ExternalLink, BookOpen, GraduationCap, Play, Search, CheckCircle2 } from 'lucide-react';
import { useState } from 'react';

export default function RoadmapCard({ step, index }) {
  const [isCompleted, setIsCompleted] = useState(false);

  const levelConfig = {
    1: { text: 'Beginner', color: 'bg-green-500', border: 'border-green-500', bg: 'bg-green-500/10' },
    2: { text: 'Beginner', color: 'bg-green-500', border: 'border-green-500', bg: 'bg-green-500/10' },
    3: { text: 'Intermediate', color: 'bg-yellow-500', border: 'border-yellow-500', bg: 'bg-yellow-500/10' },
    4: { text: 'Intermediate', color: 'bg-yellow-500', border: 'border-yellow-500', bg: 'bg-yellow-500/10' },
    5: { text: 'Advanced', color: 'bg-red-500', border: 'border-red-500', bg: 'bg-red-500/10' },
    6: { text: 'Advanced', color: 'bg-red-500', border: 'border-red-500', bg: 'bg-red-500/10' },
  };

  const stepNum = index + 1;
  const config = levelConfig[stepNum] || { text: 'Step', color: 'bg-purple-500', border: 'border-purple-500', bg: 'bg-purple-500/10' };

  const getCourseSearchUrl = (courseName) => {
    const query = encodeURIComponent(courseName + ' online course');
    return `https://www.google.com/search?q=${query}`;
  };

  return (
    <div className={`rounded-xl border-l-4 ${config.border} ${config.bg} p-5 transition-all hover:scale-[1.01] ${isCompleted ? 'opacity-60' : ''}`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={`${config.color} text-white text-xs font-medium px-2.5 py-1 rounded-full`}>
              {config.text}
            </span>
            <span className="text-purple-300 text-sm font-medium">Step {stepNum} of 6</span>
            <span className="text-purple-400 text-xs">• ~3-4 weeks</span>
          </div>
          <h3 className="text-xl font-bold text-white">{step.step_name}</h3>
        </div>
        <button
          onClick={() => setIsCompleted(!isCompleted)}
          className={`p-2 rounded-full transition-all ${isCompleted ? 'bg-green-500 text-white' : 'bg-white/10 text-purple-300 hover:bg-white/20'}`}
          title={isCompleted ? 'Mark as incomplete' : 'Mark as complete'}
        >
          <CheckCircle2 className="w-5 h-5" />
        </button>
      </div>

      {/* Resources Section */}
      <div className="space-y-4">
        {/* Official Docs */}
        {step.official_docs_url && (
          <a
            href={step.official_docs_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all font-medium text-sm shadow-lg shadow-blue-500/20"
          >
            <BookOpen className="w-4 h-4" />
            Read Official Documentation
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}

        {/* Paid Course */}
        {step.paid_course_recommendation && (
          <div className="flex items-start gap-3 p-4 bg-gradient-to-r from-orange-500/10 to-yellow-500/10 rounded-xl border border-orange-500/20">
            <div className="w-10 h-10 bg-orange-500/20 rounded-full flex items-center justify-center flex-shrink-0">
              <GraduationCap className="w-5 h-5 text-orange-400" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-orange-300 text-xs font-semibold uppercase tracking-wide mb-1">Premium Course</p>
              <p className="text-white font-medium">{step.paid_course_recommendation}</p>
              <a
                href={getCourseSearchUrl(step.paid_course_recommendation)}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 text-orange-400 hover:text-orange-300 text-sm mt-2 transition-colors font-medium"
              >
                <Search className="w-3.5 h-3.5" />
                Find this Course
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        )}

        {/* YouTube Videos */}
        {step.video_results && step.video_results.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-red-500/20 rounded-full flex items-center justify-center">
                <Play className="w-3.5 h-3.5 text-red-400" />
              </div>
              <p className="text-red-300 text-sm font-semibold">Free Video Course</p>
            </div>
            <div className="grid gap-3">
              {step.video_results.map((video, vIndex) => (
                <a
                  key={vIndex}
                  href={video.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-4 p-3 bg-gradient-to-r from-red-500/10 to-pink-500/10 rounded-xl hover:from-red-500/20 hover:to-pink-500/20 transition-all border border-red-500/20 group"
                >
                  <div className="relative">
                    <img
                      src={video.thumbnail}
                      alt=""
                      className="w-40 h-24 object-cover rounded-lg flex-shrink-0"
                    />
                    <div className="absolute inset-0 bg-black/40 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <Play className="w-8 h-8 text-white" fill="white" />
                    </div>
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-white font-medium line-clamp-2 group-hover:text-red-200 transition-colors">
                      {video.title}
                    </p>
                    <p className="text-purple-400 text-sm mt-1">{video.channel}</p>
                    <span className="inline-block mt-2 text-xs text-red-400 bg-red-500/10 px-2 py-1 rounded-full">
                      Full Course • Free
                    </span>
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Fallback */}
        {(!step.video_results || step.video_results.length === 0) && !step.official_docs_url && (
          <div className="p-3 bg-white/5 rounded-lg border border-purple-500/20">
            <p className="text-purple-400 text-sm">
              💡 Search YouTube for: <span className="text-purple-300">"{step.youtube_search_query}"</span>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
