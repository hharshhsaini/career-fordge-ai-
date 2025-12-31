import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export const generateRoadmapWithVideos = async (skills, interests) => {
  const response = await axios.post(`${API_BASE}/roadmap-with-videos`, {
    skills,
    interests,
  });
  return response.data;
};

export const getYoutubeVideos = async (query, maxResults = 3) => {
  const response = await axios.post(`${API_BASE}/youtube-videos`, {
    query,
    max_results: maxResults,
  });
  return response.data.videos;
};
