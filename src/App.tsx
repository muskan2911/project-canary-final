import { useState, useEffect } from 'react';
import { LayoutDashboard, AlertCircle, FileText, FolderOpen } from 'lucide-react';
import { StatCard } from './components/StatCard';
import { FilterBar } from './components/FilterBar';
import { CaseTable } from './components/CaseTable';
import { RelatedCasesPanel } from './components/RelatedCasesPanel';
import { TabSlider } from './components/TabSlider';
import { useCases, useDashboardStats } from './hooks/useCases';
import { Case, CaseFilters } from './types/case';

function App() {
  const [activeTab, setActiveTab] = useState('all');
  const [filters, setFilters] = useState<CaseFilters>({});
  const [selectedCase, setSelectedCase] = useState<Case | null>(null);
  const { stats, loading: statsLoading } = useDashboardStats();

  const tabFilters: CaseFilters = activeTab === 'all'
    ? filters
    : activeTab === 'high-priority'
    ? { ...filters, priority: undefined }
    : activeTab === 'incidents'
    ? { ...filters, type: 'Incident' }
    : activeTab === 'open'
    ? { ...filters, status: 'Open' }
    : filters;

  const { cases, loading: casesLoading } = useCases(tabFilters);

  const filteredCases = activeTab === 'high-priority'
    ? cases.filter(c => c.priority === 'High' || c.priority === 'Critical')
    : cases;

  useEffect(() => {
    document.title = 'Project Canary - Dashboard';
  }, []);

  const tabs = [
    { id: 'all', label: 'All Cases', count: stats.total_cases },
    { id: 'high-priority', label: 'High Priority', count: stats.high_priority },
    { id: 'incidents', label: 'Incidents', count: stats.incidents },
    { id: 'open', label: 'Open Cases', count: stats.open_cases },
  ];

  const handleStatCardClick = (tabId: string) => {
    setActiveTab(tabId);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-2 rounded-lg">
              <LayoutDashboard className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Project Canary</h1>
              <p className="text-sm text-gray-600">AI-Powered Case Management Dashboard</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Cases"
            value={statsLoading ? 0 : stats.total_cases}
            icon={FileText}
            color="bg-blue-600"
            onClick={() => handleStatCardClick('all')}
          />
          <StatCard
            title="High Priority"
            value={statsLoading ? 0 : stats.high_priority}
            icon={AlertCircle}
            color="bg-orange-600"
            onClick={() => handleStatCardClick('high-priority')}
          />
          <StatCard
            title="Incidents"
            value={statsLoading ? 0 : stats.incidents}
            icon={AlertCircle}
            color="bg-red-600"
            onClick={() => handleStatCardClick('incidents')}
          />
          <StatCard
            title="Open Cases"
            value={statsLoading ? 0 : stats.open_cases}
            icon={FolderOpen}
            color="bg-green-600"
            onClick={() => handleStatCardClick('open')}
          />
        </div>

        <TabSlider tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />

        <FilterBar filters={filters} onFilterChange={setFilters} />

        {casesLoading ? (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-500">Loading cases...</p>
          </div>
        ) : (
          <>
            <div className="mb-4 flex items-center justify-between">
              <p className="text-sm text-gray-600">
                Showing <span className="font-semibold">{filteredCases.length}</span> cases
              </p>
            </div>
            <CaseTable
              cases={filteredCases}
              onSelectCase={setSelectedCase}
              selectedCaseId={selectedCase?.id}
            />
          </>
        )}
      </main>

      {selectedCase && (
        <>
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
            onClick={() => setSelectedCase(null)}
          />
          <RelatedCasesPanel
            selectedCase={selectedCase}
            onClose={() => setSelectedCase(null)}
          />
        </>
      )}
    </div>
  );
}

export default App;
