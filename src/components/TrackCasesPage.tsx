import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Case } from '../types/case';
import { CaseTable } from './CaseTable';

export default function TrackCasesPage() {
  const { trackId } = useParams();
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(false);
  const [trackName, setTrackName] = useState('');

  useEffect(() => {
    const fetchCases = async () => {
      setLoading(true);
      // Step 1: Get case IDs for the track
      const res = await axios.get(`/api/tracks/${trackId}/cases`);
      const caseIdList = Array.isArray(res.data) ? res.data.map((c: any) => c.case_id) : [];
      setTrackName(trackId); // fallback, since track_name is not available
      // Step 2: Fetch full details for each case
      const caseDetails = await Promise.all(
        caseIdList.map(async (caseId: string) => {
          try {
            const detailRes = await axios.get(`/api/cases/${caseId}`);
            return detailRes.data;
          } catch {
            return { case_id: caseId }; // fallback if fetch fails
          }
        })
      );
      setCases(caseDetails);
      setLoading(false);
    };
    if (trackId) fetchCases();
  }, [trackId]);

  return (
    <div className="max-w-5xl mx-auto py-8 px-4">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-2">Track: {trackName || trackId}</h2>
        <p className="text-gray-600">Showing all cases for this track.</p>
      </div>
      {loading ? (
        <div className="bg-white rounded-lg shadow-sm p-12 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">Loading cases...</p>
        </div>
      ) : (
        <CaseTable cases={cases} onSelectCase={() => {}} />
      )}
    </div>
  );
}
