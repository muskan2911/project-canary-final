import { useState, useEffect } from 'react';
import { Case, DashboardStats, SimilarCase, CaseFilters } from '../types/case';

const API_BASE = '/api';

export function useCases(filters?: CaseFilters) {
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCases();
  }, [filters]);

  async function fetchCases() {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value) params.append(key, value);
        });
      }
      const res = await fetch(`${API_BASE}/cases?${params.toString()}`);
      const data = await res.json();
      setCases(data.cases || []);
      setError(null);
    } catch (err) {
      setError('Failed to fetch cases');
    } finally {
      setLoading(false);
    }
  }

  return { cases, loading, error };
}

export function useDashboardStats() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  async function fetchStats() {
    const res = await fetch(`${API_BASE}/stats`);
    const data = await res.json();
    setStats(data);
    setLoading(false);
  }

  return { stats, loading };
}

export function useSimilarCases(caseId: string) {
  const [similarCases, setSimilarCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!caseId) {
      setError('No case ID provided');
      setLoading(false);
      return;
    }
    fetchSimilar();
  }, [caseId]);

  async function fetchSimilar() {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE}/cases/${caseId}/similar`);
      if (!res.ok) {
        throw new Error(`Failed to fetch related cases: ${res.status}`);
      }
      const data = await res.json();
      setSimilarCases(data.similar_cases || []);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch related cases');
      setSimilarCases([]);
    } finally {
      setLoading(false);
    }
  }

  return { similarCases, loading, error };
}

export async function fetchProducts(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/products`);
  const data = await res.json();
  return data.products || [];
}

export async function fetchTypes(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/types`);
  const data = await res.json();
  return data.types || [];
}

export async function fetchPriorities(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/priorities`);
  const data = await res.json();
  return data.priorities || [];
}
