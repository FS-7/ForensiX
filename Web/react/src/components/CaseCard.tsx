import { CrimeCase } from "@/types/case";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, MapPin, User, AlertCircle } from "lucide-react";
import { Link } from "react-router-dom";

interface CaseCardProps {
  case_: CrimeCase;
}

export const CaseCard = ({ case_ }: CaseCardProps) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "open":
        return "bg-info text-info-foreground";
      case "investigating":
        return "bg-warning text-warning-foreground";
      case "pending":
        return "bg-secondary text-secondary-foreground";
      case "solved":
        return "bg-success text-success-foreground";
      case "closed":
        return "bg-muted text-muted-foreground";
      default:
        return "bg-secondary text-secondary-foreground";
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-accent text-accent-foreground";
      case "high":
        return "bg-destructive text-destructive-foreground";
      case "medium":
        return "bg-warning text-warning-foreground";
      case "low":
        return "bg-muted text-muted-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  return (
    <Link to={`/cases/${case_.id}`}>
      <Card className="p-6 hover:shadow-lg transition-shadow cursor-pointer">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-1">{case_.title}</h3>
            <p className="text-sm text-muted-foreground">{case_.caseNumber}</p>
          </div>
          <div className="flex gap-2">
            <Badge className={getSeverityColor(case_.severity)}>
              {case_.severity}
            </Badge>
            <Badge className={getStatusColor(case_.status)}>
              {case_.status}
            </Badge>
          </div>
        </div>
        
        <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
          {case_.description}
        </p>
        
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2 text-muted-foreground">
            <MapPin className="h-4 w-4" />
            <span>{case_.location}</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Calendar className="h-4 w-4" />
            <span>Reported: {new Date(case_.dateReported).toLocaleDateString()}</span>
          </div>
          {case_.assignedOfficer && (
            <div className="flex items-center gap-2 text-muted-foreground">
              <User className="h-4 w-4" />
              <span>{case_.assignedOfficer}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-muted-foreground">
            <AlertCircle className="h-4 w-4" />
            <span className="capitalize">{case_.type}</span>
          </div>
        </div>
      </Card>
    </Link>
  );
};
