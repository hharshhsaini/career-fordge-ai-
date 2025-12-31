import { Briefcase, BookOpen, Play, ExternalLink, GraduationCap, Clock, Eye } from 'lucide-react';

export default function RoadmapDisplay({ data }) {
  if (!data) return null;

  const levelColors = {
    Beginner: 'bg-green-500',
    Intermediate: 'bg-yellow-500',
    Advanced: 'bg-red-500',
  };

  return (
    <div className="space-y-6">
      {/* Career Role Card */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-6 text-white">
        <div className="flex items-center gap-3 mb-3">
          <Briefcase className="w-8 h-8" />
          <h2 className="text-2xl font-bold">Recommended Career</h2>
        </div>
        <h3 className="text-3xl font-bold mb-3">{data.career_role}</h3>
        <p className="text-purple-100">{data.explanation}</p>
      </div>

      {/* Official Resources */}
      {data.official_resources && data.official_resources.length > 0 && (
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <ExternalLink className="w-6 h-6 text-blue-400" />
            <h3 className="text-xl font-bold text-white">Official Documentation & Resources</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {data.official_resources.map((resource, idx) => (
              <a
                key={idx}
                href={resource.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 bg-blue-500/20 rounded-lg hover:bg-blue-500/30 transition-colors border border-blue-500/30"
              >
                <ExternalLink className="w-5 h-5 text-blue-400 flex-shrink-0" />
                <div>
                  <p className="text-white font-medium text-sm">{resource.name}</p>
                  <p className="text-blue-300 text-xs">{resource.type}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Learning Roadmap Timeline */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6">
        <div className="flex items-center gap-3 mb-6">
          <BookOpen className="w-6 h-6 text-purple-400" />
          <h3 className="text-xl font-bold text-white">Complete Learning Roadmap</h3>
        </div>

        <div className="space-y-6">
          {data.roadmap?.map((step, index) => (
            <div key={index} className="relative pl-8">
              {/* Timeline line */}
              {index < data.roadmap.length - 1 && (
                <div className="absolute left-3 top-8 w-0.5 h-full bg-purple-500/30" />
              )}
              
              {/* Timeline dot */}
              <div className={`absolute left-0 top-1 w-6 h-6 rounded-full ${levelColors[step.level] || 'bg-purple-500'} flex items-center justify-center text-white text-xs font-bold`}>
                {step.step || index + 1}
              </div>

              {/* Step content */}
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20">
                <div className="flex items-center gap-2 mb-2 flex-wrap">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium text-white ${levelColors[step.level] || 'bg-purple-500'}`}>
                    {step.level}
                  </span>
                  {step.duration && (
                    <span className="flex items-center gap-1 text-purple-300 text-xs">
                      <Clock className="w-3 h-3" /> {step.duration}
                    </span>
                  )}
                </div>
                
                <h4 className="text-lg font-semibold text-white mb-1">{step.topic}</h4>
                {step.description && (
                  <p className="text-purple-200 text-sm mb-4">{step.description}</p>
                )}

                {/* Resources Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mb-3">
                  {/* Official Docs */}
                  {step.official_docs && step.official_docs.url && (
                    <a
                      href={step.official_docs.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 p-2 bg-blue-500/10 rounded-lg hover:bg-blue-500/20 transition-colors border border-blue-500/20"
                    >
                      <ExternalLink className="w-4 h-4 text-blue-400 flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-xs text-blue-300">Official Docs</p>
                        <p className="text-sm text-white truncate">{step.official_docs.name}</p>
                      </div>
                    </a>
                  )}

                  {/* Paid Course */}
                  {step.paid_course && step.paid_course.name && (
                    <div className="flex items-center gap-2 p-2 bg-orange-500/10 rounded-lg border border-orange-500/20">
                      <GraduationCap className="w-4 h-4 text-orange-400 flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-xs text-orange-300">{step.paid_course.platform} {step.paid_course.instructor && `• ${step.paid_course.instructor}`}</p>
                        <p className="text-sm text-white truncate">{step.paid_course.name}</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* YouTube Videos */}
                {step.videos && step.videos.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-purple-300 text-sm flex items-center gap-1">
                      <Play className="w-4 h-4" /> Free YouTube Courses:
                    </p>
                    <div className="grid gap-2">
                      {step.videos.map((video, vIndex) => (
                        <a
                          key={vIndex}
                          href={video.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-3 p-2 bg-red-500/10 rounded-lg hover:bg-red-500/20 transition-colors group border border-red-500/20"
                        >
                          <img
                            src={video.thumbnail}
                            alt=""
                            className="w-32 h-18 object-cover rounded flex-shrink-0"
                          />
                          <div className="min-w-0 flex-1">
                            <p className="text-sm text-white group-hover:text-red-200 transition-colors line-clamp-2 font-medium">
                              {video.title}
                            </p>
                            <p className="text-xs text-purple-300 mt-1">{video.channel}</p>
                            <div className="flex items-center gap-3 mt-1 text-xs text-purple-400">
                              {video.duration && <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {video.duration}</span>}
                              {video.views && <span className="flex items-center gap-1"><Eye className="w-3 h-3" /> {video.views}</span>}
                            </div>
                          </div>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
