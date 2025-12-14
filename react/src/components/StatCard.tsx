import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  subValue?: string;
  icon: LucideIcon;
  variant?: 'default' | 'primary' | 'success' | 'warning';
}

export function StatCard({ label, value, subValue, icon: Icon, variant = 'default' }: StatCardProps) {
  return (
    <div className="card-gradient rounded-lg border border-border p-5 animate-fade-in hover:border-primary/30 transition-colors">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground mb-1">{label}</p>
          <p className={cn(
            "text-2xl font-semibold font-mono",
            variant === 'primary' && "text-primary",
            variant === 'success' && "text-success",
            variant === 'warning' && "text-warning",
            variant === 'default' && "text-foreground"
          )}>
            {value}
          </p>
          {subValue && (
            <p className="text-xs text-muted-foreground mt-1">{subValue}</p>
          )}
        </div>
        <div className={cn(
          "w-10 h-10 rounded-lg flex items-center justify-center",
          variant === 'primary' && "bg-primary/10",
          variant === 'success' && "bg-success/10",
          variant === 'warning' && "bg-warning/10",
          variant === 'default' && "bg-secondary"
        )}>
          <Icon className={cn(
            "w-5 h-5",
            variant === 'primary' && "text-primary",
            variant === 'success' && "text-success",
            variant === 'warning' && "text-warning",
            variant === 'default' && "text-muted-foreground"
          )} />
        </div>
      </div>
    </div>
  );
}
