import { ExternalLink, BookOpen, GraduationCap, Play, Search } from 'lucide-react';

export default function RoadmapCard({ step, index }) {
  const levelColors = {
    1: 'border-green-500 bg-green-500/10',
    2: 'border-green-500 bg-green-500/10',
    3: 'border-yellow-500 bg-yellow-500/10',
    4: 'border-yellow-500 bg-yellow-500/10',
    5: 'border-red-500 bg-red-500/10',
    6: 'border-red-500 bg-red-500/10',
  };

  const levelBadge = {
    1: { text: 'Beginner', color: 'bg-green-500' },
    2: { text: 'Beginner', color: 'bg-green-500' },
    3: { text: 'Intermediate', color: 'bg-yellow-500' },
    4: { text: 'Intermediate', color: 'bg-yellow-500' },
    5: { text: 'Advanced', color: 'bg-red-500' },
    6: { text: 'Advanced', color: 'bg-red-500' },
  };

  const stepNum = index + 1;
  const badge = levelBadge[stepNum] || { text: 'Step', color: 'bg-purple-500' };

  // Generate course search URL (searches across all platforms)
  const getCourseSearchUrl = (courseName) => {
    const query = encodeURIComponent(courseName + ' online course');
    return `https://www.google.com/search?q=${query}`;
  };

  return (
    <div className={`rounded-xl border-l-4 ${levelColors[stepNum] || 'border-purple-500 bg-purple-500/10'} p-5`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-4 mb-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className={`${badge.color} text-white text-xs font-medium px-2 py-1 rounded-full`}>
              {badge.text}
            </span>
            <span className="text-purple-300 text-sm">Step {stepNum}</span>
          </div>
          <h3 className="text-xl font-bold text-white">{step.step_name}</h3>
        </div>
      </div>

      {/* Resources Section */}
      <div className="space-y-4">
        {/* Official Docs Badge */}
        {step.official_docs_url && (
          <a
            href={step.official_docs_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium text-sm"
          >
            <BookOpen className="w-4 h-4" />
            Read Official Docs
            <ExternalLink className="w-3 h-3" />
          </a>
        )}

        {/* Paid Course Recommendation */}
        {step.paid_course_recommendation && (
          <div className="flex items-start gap-3 p-3 bg-white/5 rounded-lg border border-orange-500/20">
            <GraduationCap className="w-5 h-5 text-orange-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1 min-w-0">
              <p className="text-orange-300 text-xs font-medium mb-1">Top Rated Course</p>
              <p className="text-white text-sm">{step.paid_course_recommendation}</p>
              <a
                href={getCourseSearchUrl(step.paid_course_recommendation)}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-orange-400 hover:text-orange-300 text-xs mt-2 transition-colors"
              >
                <Search className="w-3 h-3" />
                Find this Course
              </a>
            </div>
          </div>
        )}

        {/* Free Video Lectures */}
        {step.video_results && step.video_results.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Play className="w-4 h-4 text-red-400" />
              <p className="text-red-300 text-sm font-medium">Free Video Lectures</p>
            </div>
            <div className="grid gap-3">
              {step.video_results.map((video, vIndex) => (
                <a
                  key={vIndex}
                  href={video.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-4 p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors border border-red-500/20 group"
                >
                  <img
                    src={video.thumbnail}
                    alt=""
                    className="w-36 h-20 object-cover rounded flex-shrink-0"
                  />
                  <div className="min-w-0 flex-1">
                    <p className="text-white text-sm font-medium line-clamp-2 group-hover:text-red-200 transition-colors">
                      {video.title}
                    </p>
                    <p className="text-purple-400 text-xs mt-1">{video.channel}</p>
                  </div>
                </a>
              ))}
            </div>
          </div>
        )}

        {/* Fallback if no videos */}
        {(!step.video_results || step.video_results.length === 0) && !step.official_docs_url && (
          <p className="text-purple-400 text-sm italic">
            Search YouTube for: "{step.youtube_search_query}"
          </p>
        )}
      </div>
    </div>
  );
}
