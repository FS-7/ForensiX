export type CaseStatus = "open" | "investigating" | "pending" | "closed" | "solved";
export type CaseSeverity = "low" | "medium" | "high" | "critical";
export type CaseType = "theft" | "assault" | "fraud" | "vandalism" | "homicide" | "cybercrime" | "other";

export interface CrimeCase {
  id: string;
  caseNumber: string;
  title: string;
  description: string;
  type: CaseType;
  status: CaseStatus;
  severity: CaseSeverity;
  location: string;
  dateReported: string;
  dateOccurred: string;
  assignedOfficer?: string;
  witnesses?: number;
  evidences?: string[];
  notes?: string;
}
