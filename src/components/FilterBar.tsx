import { Search, X } from 'lucide-react';
import { useState, useEffect } from 'react';
import { CaseFilters } from '../types/case';
import { fetchProducts, fetchTypes, fetchPriorities } from '../hooks/useCases';

interface FilterBarProps {
  filters: CaseFilters;
  onFilterChange: (filters: CaseFilters) => void;
}

export function FilterBar({ filters, onFilterChange }: FilterBarProps) {
  const [products, setProducts] = useState<string[]>([]);
  const [types, setTypes] = useState<string[]>([]);
  const [priorities, setPriorities] = useState<string[]>([]);
  const [localFilters, setLocalFilters] = useState<CaseFilters>(filters);

  useEffect(() => {
    fetchProducts().then(setProducts);
    fetchTypes().then(setTypes);
    fetchPriorities().then(setPriorities);
  }, []);

  const handleChange = (key: keyof CaseFilters, value: string) => {
    const newFilters = { ...localFilters, [key]: value || undefined };
    setLocalFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    const emptyFilters: CaseFilters = {};
    setLocalFilters(emptyFilters);
    onFilterChange(emptyFilters);
  };

  const hasActiveFilters = Object.values(localFilters).some(v => v);

  return (
    <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
      <div className="flex items-center gap-2 mb-3">
        <Search className="w-5 h-5 text-gray-400" />
        <h3 className="text-sm font-semibold text-gray-700">Filters</h3>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="ml-auto text-sm text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            <X className="w-4 h-4" />
            Clear
          </button>
        )}
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <input
          type="text"
          placeholder="Customer Name"
          value={localFilters.customer_name || ''}
          onChange={e => handleChange('customer_name', e.target.value)}
          className="input input-bordered w-full"
        />
        <input
          type="text"
          placeholder="Case ID"
          value={localFilters.case_id || ''}
          onChange={e => handleChange('case_id', e.target.value)}
          className="input input-bordered w-full"
        />
        <select
          value={localFilters.product || ''}
          onChange={e => handleChange('product', e.target.value)}
          className="input input-bordered w-full"
        >
          <option value="">Product</option>
          {products.map(product => (
            <option key={product} value={product}>{product}</option>
          ))}
        </select>
        <select
          value={localFilters.priority || ''}
          onChange={e => handleChange('priority', e.target.value)}
          className="input input-bordered w-full"
        >
          <option value="">Priority</option>
          {priorities.map(priority => (
            <option key={priority} value={priority}>{priority}</option>
          ))}
        </select>
        <select
          value={localFilters.type || ''}
          onChange={e => handleChange('type', e.target.value)}
          className="input input-bordered w-full"
        >
          <option value="">Type</option>
          {types.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
        <select
          value={localFilters.status || ''}
          onChange={e => handleChange('status', e.target.value)}
          className="input input-bordered w-full"
        >
          <option value="">Status</option>
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Resolved">Resolved</option>
          <option value="Closed">Closed</option>
        </select>
      </div>
    </div>
  );
}
