import { X, Link2, TrendingUp } from 'lucide-react';
import { Case, SimilarCase } from '../types/case';
import { useSimilarCases } from '../hooks/useCases';
import { Link } from 'react-router-dom';

interface RelatedCasesPanelProps {
  selectedCase: Case;
  onClose: () => void;
}

export function RelatedCasesPanel({ selectedCase, onClose }: RelatedCasesPanelProps) {
  const caseId = selectedCase.case_id;
  const { similarCases, loading, error } = useSimilarCases(caseId);
  const casesArray = Array.isArray(similarCases) ? similarCases : [];
  const relatedCount = casesArray.length;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical':
        return 'text-red-600';
      case 'High':
        return 'text-orange-600';
      case 'Medium':
        return 'text-yellow-600';
      case 'Low':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-96 bg-white shadow-2xl z-50 flex flex-col">
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Case Details</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-white/20 rounded transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="space-y-2">
          <p className="text-sm opacity-90">Case ID</p>
          <p className="font-mono text-lg font-semibold">{selectedCase.case_id}</p>
          {/* Show Jira ID if present */}
          {selectedCase.jira_id && (
            <div>
              <p className="text-sm opacity-90">Jira ID</p>
              <p className="font-mono text-blue-700">{selectedCase.jira_id}</p>
            </div>
          )}
          {/* Show Snow ID if present */}
          {selectedCase.snow_id && (
            <div>
              <p className="text-sm opacity-90">Snow ID</p>
              <p className="font-mono text-purple-700">{selectedCase.snow_id}</p>
            </div>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="space-y-6">
          <div>
            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Customer
            </label>
            <p className="mt-1 text-gray-900 font-medium">{selectedCase.customer_name}</p>
          </div>

          <div>
            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Description
            </label>
            <p className="mt-1 text-gray-700 text-sm leading-relaxed">
              {selectedCase.description}
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Priority
              </label>
              <p className={`mt-1 font-semibold ${getPriorityColor(selectedCase.priority)}`}>
                {selectedCase.priority}
              </p>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Status
              </label>
              <p className="mt-1 text-gray-900 font-medium">{selectedCase.status}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Type
              </label>
              <p className="mt-1 text-gray-900">{selectedCase.type}</p>
            </div>

            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Product
              </label>
              <p className="mt-1 text-gray-900">{selectedCase.product}</p>
            </div>
          </div>

          {selectedCase.module && (
            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Module
              </label>
              <p className="mt-1 text-gray-900">{selectedCase.module}</p>
              {selectedCase.sub_module && (
                <p className="text-sm text-gray-600">{selectedCase.sub_module}</p>
              )}
            </div>
          )}

          {selectedCase.category && (
            <div>
              <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Category
              </label>
              <p className="mt-1 text-gray-900">{selectedCase.category}</p>
            </div>
          )}

          <div>
            <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Created
            </label>
            <p className="mt-1 text-gray-900">{formatDate(selectedCase.created_date)}</p>
          </div>

          <div className="border-t pt-6">
            <div className="flex items-center gap-2 mb-4">
              <Link2 className="w-5 h-5 text-blue-600" />
              <h3 className="font-semibold text-gray-900">
                Related Cases{relatedCount > 0 ? ` (${relatedCount})` : ''}
              </h3>
            </div>
            {/* Guard for missing caseId */}
            {!caseId ? (
              <div className="text-center py-8 text-red-600">
                <p>No case ID available for related cases.</p>
              </div>
            ) : loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              </div>
            ) : error ? (
              <div className="text-center py-8 text-red-600">
                <p>{error}</p>
              </div>
            ) : casesArray.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>No related cases found.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {casesArray.map((similar, idx) => (
                  <div
                    key={similar.case_id || idx}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors mb-2"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <Link
                        to={`/case/${similar.case_id}`}
                        className="font-medium text-blue-600 hover:underline"
                      >
                        {similar.case_id || 'Unknown Case ID'}
                      </Link>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{similar.customer_name || 'Unknown Customer'}</p>
                    <p className="text-xs text-gray-500 line-clamp-2">
                      {similar.description || 'No description available.'}
                    </p>
                    <div className="flex gap-2 mt-3">
                      <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                        {similar.type || 'Unknown'}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(similar.priority)} bg-opacity-10`}>
                        {similar.priority || 'Unknown'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
