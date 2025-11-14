export interface Case {
  id: string;
  case_id: string;
  customer_name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  type: 'Inquiry' | 'Incident' | 'Jira' | 'Bug' | 'Feature Request';
  product: string;
  status: 'Open' | 'In Progress' | 'Resolved' | 'Closed';
  module?: string;
  sub_module?: string;
  category?: string;
  geography?: string;
  created_date: string;
  updated_date: string;
}

export interface SimilarCase {
  related_case_id: string;
  similarity_score: number;
  cases: Case;
}

export interface DashboardStats {
  total_cases: number;
  high_priority: number;
  incidents: number;
  open_cases: number;
}

export interface CaseFilters {
  customer_name?: string;
  case_id?: string;
  product?: string;
  priority?: string;
  type?: string;
  status?: string;
}
