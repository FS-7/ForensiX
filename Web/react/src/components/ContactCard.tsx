import { Phone, AlertTriangle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface ContactCardProps {
  number: string;
  label?: string;
  isThreat?: boolean;
  className?: string;
}

export const ContactCard = ({ number, label, isThreat = false, className }: ContactCardProps) => {
  return (
    <Card 
      className={cn(
        "transition-all hover:shadow-lg",
        isThreat && "border-threat bg-threat-bg",
        className
      )}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3 flex-1">
            <div className={cn(
              "rounded-full p-2.5 transition-colors",
              isThreat ? "bg-threat/10" : "bg-primary/10"
            )}>
              <Phone className={cn(
                "h-5 w-5",
                isThreat ? "text-threat" : "text-primary"
              )} />
            </div>
            <div className="flex-1 min-w-0">
              
              <p className={cn(
                "text-lg font-semibold",
                isThreat && "text-threat"
              )}>
                {number}
              </p>
            </div>
          </div>
          {isThreat && (
            <Badge variant="destructive" className="flex items-center gap-1">
              <AlertTriangle className="h-3 w-3" />
              <p className={cn(
                "text-sm font-medium mb-1",
                isThreat ? "text-threat" : "text-muted-foreground"
              )}>
                {label}
              </p>
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
