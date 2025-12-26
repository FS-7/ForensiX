import { useState, useMemo } from "react";
import { FilterBar } from "@/components/FilterBar";
import { PhoneIncoming, PhoneOutgoing, PhoneMissed, Phone } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const callTypeIcons = {
  incoming: PhoneIncoming,
  outgoing: PhoneOutgoing,
  missed: PhoneMissed,
  rejected: PhoneMissed
};

const callTypeColors = {
  incoming: "text-success",
  outgoing: "text-primary",
  missed: "text-destructive",
  rejected: "text-destructive",
};

export interface CallLog {
  id: string;
  Name: string;
  Number: string;
  Call_logs: []
  Tags: []
}

export function CallLogs({ report }) {
  const [callLogs, setCallLogs] = useState(report[0]["Call_logs"] || [])

  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [dateFilter, setDateFilter] = useState("all");

  const formatDuration = (seconds: number) => {
    if (seconds === 0) return "-";
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return `Today, ${date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
    if (diffDays === 1) return `Yesterday, ${date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  const filteredLogs = useMemo(() => {
    return callLogs.filter((log) => {
      const matchesSearch =
        (log.Name && log.Name.toLowerCase().includes(search.toLowerCase())) ||
        log.Number.includes(search);

      const matchesType = typeFilter === "all" || typeFilter === log.Call_logs.Type.toLowerCase();

      let matchesDate = true;
      if (dateFilter !== "all") {
        const logDate = new Date(log.Call_logs.Datetime);
        const now = new Date();
        const diffDays = Math.floor((now.getTime() - logDate.getTime()) / (1000 * 60 * 60 * 24));

        if (dateFilter === "today") matchesDate = diffDays === 0;
        if (dateFilter === "week") matchesDate = diffDays <= 7;
        if (dateFilter === "month") matchesDate = diffDays <= 30;
      }

      return matchesSearch && matchesType && matchesDate;
    });
  }, [search, typeFilter, dateFilter]);

  /*
  const groupedByNumber = useMemo(() => {
    const groups: Record<string, { Name: string; Number: string; Call_logs: typeof filteredLogs }> = {};

    filteredLogs.forEach((log) => {
      if (!groups[log.Number]) {
        groups[log.Number] = {
          Name: log.Name || "Unknown",
          Number: log.Number,
          Call_logs: [],
        };
      }
      groups[log.Number].Call_logs.push(log);
    });

    return Object.values(groups).sort((a, b) => {
      const latestA = Math.max(...a.Call_logs.map(l => new Date(l.Call_logs.Datetime).getTime()));
      const latestB = Math.max(...b.Call_logs.map(l => new Date(l.Call_logs.Datetime).getTime()));
      return latestB - latestA;
    });
  }, [filteredLogs]);
  */
  
  const hasActiveFilters = search !== "" || typeFilter !== "all" || dateFilter !== "all";

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Call Logs</h2>
        <p className="text-muted-foreground">View and filter your call history</p>
      </div>

      <FilterBar
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search by name or number..."
        hasActiveFilters={hasActiveFilters}
        onClearFilters={() => {
          setSearch("");
          setTypeFilter("all");
          setDateFilter("all");
        }}
        filters={[
          {
            id: "type",
            label: "Call Type",
            value: typeFilter,
            onChange: setTypeFilter,
            options: [
              { value: "all", label: "All Types" },
              { value: "incoming", label: "Incoming" },
              { value: "outgoing", label: "Outgoing" },
              { value: "missed", label: "Missed" },
              { value: "rejected", label: "Rejected" }
            ],
          },
          {
            id: "date",
            label: "Date Range",
            value: dateFilter,
            onChange: setDateFilter,
            options: [
              { value: "all", label: "All Time" },
              { value: "today", label: "Today" },
              { value: "week", label: "This Week" },
              { value: "month", label: "This Month" },
            ],
          },
        ]}
      />

      <div className="card-gradient rounded-lg border border-border overflow-hidden animate-fade-in">
        {filteredLogs.length > 0 ? (
          <Accordion type="multiple" className="w-full">
            {filteredLogs.map((log) => (
              <AccordionItem key={log.Number} value={log.Number} className="border-border">
                <AccordionTrigger className="px-4 py-3 hover:bg-secondary/50 hover:no-underline">
                  <div className="flex items-center gap-4 w-full">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                      <Phone className="w-4 h-4 text-primary" />
                    </div>
                    <div className="flex-1 text-left">
                      <p className="font-medium text-foreground">{log.Name || "Unknown" }</p>
                      <p className="text-sm font-mono text-muted-foreground">{log.Number}</p>
                    </div>
                    <Badge variant="secondary" className="mr-4">
                      {log.Call_logs.length} call{log.Call_logs.length !== 1 ? 's' : ''}
                    </Badge>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-3">
                  <div className="space-y-2 mt-2">
                    {log.Call_logs.map((log, i) => {
                      const Icon = callTypeIcons[log.Type.toLowerCase()];
                      return (
                        <div
                          key={i}
                          className="flex items-center gap-4 p-3 rounded-lg bg-secondary/30 border border-border/50"
                        >
                          <div className="flex items-center gap-2">
                            <Icon className={cn("w-4 h-4", callTypeColors[log.Type.toLowerCase()])} />
                            <Badge variant="outline" className={cn(
                              "text-xs capitalize",
                              log.Type === "missed" && "border-destructive/50 text-destructive"
                            )}>
                              {log.Type}
                            </Badge>
                          </div>
                          <div className="flex-1" />
                          <span className="font-mono text-sm text-muted-foreground">
                            {formatDuration(log.Duration)}
                          </span>
                          <span className="text-sm text-muted-foreground">
                            {formatDate(log.Datetime)}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        ) : (
          <div className="p-8 text-center text-muted-foreground">
            No call logs found matching your filters.
          </div>
        )}
      </div>
    </div>
  );
}
