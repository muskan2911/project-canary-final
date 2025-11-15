import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface Track {
  track_id: string;
  track_name: string;
}

export default function TrackManager() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [trackName, setTrackName] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchTracks = async () => {
    setLoading(true);
    const res = await axios.get('/api/tracks');
    setTracks(res.data);
    setLoading(false);
  };

  const createTrack = async () => {
    if (!trackName) return;
    await axios.post('/api/tracks', { track_name: trackName });
    setTrackName('');
    fetchTracks();
  };

  useEffect(() => {
    fetchTracks();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Track Management</h2>
      <div className="mb-4 flex gap-2">
        <input
          type="text"
          value={trackName}
          onChange={e => setTrackName(e.target.value)}
          placeholder="Track Name"
          className="border px-2 py-1 rounded"
        />
        <button onClick={createTrack} className="bg-blue-600 text-white px-4 py-1 rounded">Create Track</button>
      </div>
      {loading ? <div>Loading tracks...</div> : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {tracks.map(track => (
            <div
              key={track.track_id}
              className="bg-white bg-opacity-30 backdrop-blur-md rounded-xl shadow-lg p-6 cursor-pointer border border-gray-200 hover:scale-105 transition-transform duration-200"
              onClick={() => navigate(`/track/${track.track_id}`)}
              style={{ boxShadow: '0 4px 30px rgba(0, 0, 0, 0.1)' }}
            >
              <div className="text-lg font-semibold text-gray-800 mb-2">{track.track_name}</div>
              <div className="text-sm text-gray-600">Track ID: {track.track_id}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
