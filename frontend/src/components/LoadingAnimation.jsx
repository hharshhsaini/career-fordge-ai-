import { useState, useEffect } from 'react';

const loadingMessages = [
  "🔍 Analyzing your skills...",
  "🧠 AI is thinking...",
  "📚 Finding best resources...",
  "🎯 Matching career paths...",
  "📺 Searching quality tutorials...",
  "✨ Crafting your roadmap...",
  "🚀 Almost there..."
];

export default function LoadingAnimation() {
  const [messageIndex, setMessageIndex] = useState(0);
  const [dots, setDots] = useState('');

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setMessageIndex(prev => (prev + 1) % loadingMessages.length);
    }, 3000);

    const dotsInterval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 400);

    return () => {
      clearInterval(messageInterval);
      clearInterval(dotsInterval);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-slate-900/95 backdrop-blur-md z-50 flex items-center justify-center">
      <div className="text-center">
        {/* 3D Animated Cube */}
        <div className="scene mb-8">
          <div className="cube">
            <div className="cube-face front">
              <span className="text-3xl">🎯</span>
            </div>
            <div className="cube-face back">
              <span className="text-3xl">💼</span>
            </div>
            <div className="cube-face right">
              <span className="text-3xl">🚀</span>
            </div>
            <div className="cube-face left">
              <span className="text-3xl">📚</span>
            </div>
            <div className="cube-face top">
              <span className="text-3xl">⭐</span>
            </div>
            <div className="cube-face bottom">
              <span className="text-3xl">💡</span>
            </div>
          </div>
        </div>

        {/* Orbiting Particles */}
        <div className="orbit-container mb-6">
          <div className="orbit">
            <div className="particle particle-1"></div>
            <div className="particle particle-2"></div>
            <div className="particle particle-3"></div>
          </div>
          <div className="orbit orbit-reverse">
            <div className="particle particle-4"></div>
            <div className="particle particle-5"></div>
          </div>
        </div>

        {/* Loading Text */}
        <h2 className="text-2xl font-bold text-white mb-2">
          Career Forge
        </h2>
        <p className="text-purple-300 text-lg mb-4 h-8">
          {loadingMessages[messageIndex]}{dots}
        </p>

        {/* Progress Bar */}
        <div className="w-64 mx-auto">
          <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 rounded-full animate-loading-bar"></div>
          </div>
        </div>

        {/* Tip */}
        <p className="text-purple-400/60 text-sm mt-6 max-w-xs mx-auto">
          💡 Tip: We're finding the best courses and tutorials just for you!
        </p>
      </div>

      <style>{`
        .scene {
          width: 100px;
          height: 100px;
          perspective: 400px;
          margin: 0 auto;
        }

        .cube {
          width: 100%;
          height: 100%;
          position: relative;
          transform-style: preserve-3d;
          animation: rotateCube 4s infinite ease-in-out;
        }

        .cube-face {
          position: absolute;
          width: 100px;
          height: 100px;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid rgba(168, 85, 247, 0.4);
          background: linear-gradient(135deg, rgba(168, 85, 247, 0.2), rgba(99, 102, 241, 0.2));
          backdrop-filter: blur(10px);
          border-radius: 12px;
        }

        .front  { transform: rotateY(0deg) translateZ(50px); }
        .back   { transform: rotateY(180deg) translateZ(50px); }
        .right  { transform: rotateY(90deg) translateZ(50px); }
        .left   { transform: rotateY(-90deg) translateZ(50px); }
        .top    { transform: rotateX(90deg) translateZ(50px); }
        .bottom { transform: rotateX(-90deg) translateZ(50px); }

        @keyframes rotateCube {
          0%, 100% { transform: rotateX(-20deg) rotateY(0deg); }
          25% { transform: rotateX(-20deg) rotateY(90deg); }
          50% { transform: rotateX(-20deg) rotateY(180deg); }
          75% { transform: rotateX(-20deg) rotateY(270deg); }
        }

        .orbit-container {
          position: relative;
          width: 120px;
          height: 120px;
          margin: 0 auto;
        }

        .orbit {
          position: absolute;
          inset: 0;
          border: 1px dashed rgba(168, 85, 247, 0.3);
          border-radius: 50%;
          animation: spin 3s linear infinite;
        }

        .orbit-reverse {
          animation: spin 4s linear infinite reverse;
          inset: 15px;
        }

        .particle {
          position: absolute;
          width: 10px;
          height: 10px;
          background: linear-gradient(135deg, #a855f7, #6366f1);
          border-radius: 50%;
          box-shadow: 0 0 15px rgba(168, 85, 247, 0.6);
        }

        .particle-1 { top: -5px; left: 50%; transform: translateX(-50%); }
        .particle-2 { bottom: -5px; left: 50%; transform: translateX(-50%); }
        .particle-3 { top: 50%; right: -5px; transform: translateY(-50%); }
        .particle-4 { top: -5px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #ec4899, #f43f5e); }
        .particle-5 { bottom: -5px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #ec4899, #f43f5e); }

        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        @keyframes loading-bar {
          0% { transform: translateX(-100%); }
          50% { transform: translateX(0%); }
          100% { transform: translateX(100%); }
        }

        .animate-loading-bar {
          animation: loading-bar 1.5s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}
