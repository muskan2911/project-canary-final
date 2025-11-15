import { Case } from '../types/case';
import { ExternalLink, Clock } from 'lucide-react';

interface CaseTableProps {
  cases: Case[];
  onSelectCase: (caseItem: Case) => void;
  selectedCaseId?: string;
}

export function CaseTable({ cases, onSelectCase, selectedCaseId }: CaseTableProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical':
        return 'bg-red-100 text-red-800';
      case 'High':
        return 'bg-orange-100 text-orange-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'Low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open':
        return 'bg-blue-100 text-blue-800';
      case 'In Progress':
        return 'bg-purple-100 text-purple-800';
      case 'Resolved':
        return 'bg-green-100 text-green-800';
      case 'Closed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Incident':
        return 'bg-red-50 text-red-700 border-red-200';
      case 'Bug':
        return 'bg-orange-50 text-orange-700 border-orange-200';
      case 'Jira':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Feature Request':
        return 'bg-green-50 text-green-700 border-green-200';
      case 'Inquiry':
        return 'bg-gray-50 text-gray-700 border-gray-200';
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200';
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

  // Check if cases have more than just case_id
  const hasFullData = cases.length > 0 && Object.keys(cases[0]).length > 1;

  if (!hasFullData) {
    // Render simplified table with only case_id
    return (
      <table className="min-w-full border">
        <thead>
          <tr>
            <th className="border px-2 py-1">Case ID</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.case_id}>
              <td className="border px-2 py-1">{c.case_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  if (cases.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm p-12 text-center">
        <Clock className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <p className="text-gray-500">No cases found</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Case ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Customer
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Priority
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Created
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Jira/Snow ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {cases.map((caseItem) => (
              <tr
                key={caseItem.id}
                className={`hover:bg-gray-50 transition-colors ${
                  selectedCaseId === caseItem.id ? 'bg-blue-50' : ''
                }`}
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  <a
                    href={`/case/${caseItem.case_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-700 underline hover:text-blue-900"
                  >
                    {caseItem.case_id}
                  </a>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {caseItem.customer_name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getPriorityColor(
                      caseItem.priority
                    )}`}
                  >
                    {caseItem.priority}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded border ${getTypeColor(
                      caseItem.type
                    )}`}
                  >
                    {caseItem.type}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {caseItem.product}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span
                    className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(
                      caseItem.status
                    )}`}
                  >
                    {caseItem.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatDate(caseItem.created_date)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {caseItem.jira_id || caseItem.snow_id ? (
                    <>
                      {caseItem.jira_id && (
                        <a
                          href={`https://jira.example.com/browse/${caseItem.jira_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-blue-700 font-mono underline hover:text-blue-900"
                        >
                          {caseItem.jira_id}
                        </a>
                      )}
                      {caseItem.snow_id && (
                        <a
                          href={`https://snow.example.com/incident/${caseItem.snow_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block text-purple-700 font-mono underline hover:text-purple-900"
                        >
                          {caseItem.snow_id}
                        </a>
                      )}
                    </>
                  ) : (
                    <span className="text-gray-400">-</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <button
                    onClick={() => onSelectCase(caseItem)}
                    className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
