import { useState, useMemo } from "react";
import { callLogs, CallLog } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { PhoneIncoming, PhoneOutgoing, PhoneMissed } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

const callTypeIcons = {
  incoming: PhoneIncoming,
  outgoing: PhoneOutgoing,
  missed: PhoneMissed,
};

const callTypeColors = {
  incoming: "text-success",
  outgoing: "text-primary",
  missed: "text-destructive",
};

export function CallLogs() {
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
        log.contactName.toLowerCase().includes(search.toLowerCase()) ||
        log.phoneNumber.includes(search);
      
      const matchesType = typeFilter === "all" || log.type === typeFilter;
      
      let matchesDate = true;
      if (dateFilter !== "all") {
        const logDate = new Date(log.timestamp);
        const now = new Date();
        const diffDays = Math.floor((now.getTime() - logDate.getTime()) / (1000 * 60 * 60 * 24));
        
        if (dateFilter === "today") matchesDate = diffDays === 0;
        if (dateFilter === "week") matchesDate = diffDays <= 7;
        if (dateFilter === "month") matchesDate = diffDays <= 30;
      }
      
      return matchesSearch && matchesType && matchesDate;
    });
  }, [search, typeFilter, dateFilter]);

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
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead className="text-muted-foreground">Type</TableHead>
              <TableHead className="text-muted-foreground">Contact</TableHead>
              <TableHead className="text-muted-foreground">Number</TableHead>
              <TableHead className="text-muted-foreground">Duration</TableHead>
              <TableHead className="text-muted-foreground">Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredLogs.map((log) => {
              const Icon = callTypeIcons[log.type];
              return (
                <TableRow key={log.id} className="border-border hover:bg-secondary/50">
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Icon className={cn("w-4 h-4", callTypeColors[log.type])} />
                      <Badge variant="outline" className={cn(
                        "text-xs capitalize",
                        log.type === "missed" && "border-destructive/50 text-destructive"
                      )}>
                        {log.type}
                      </Badge>
                    </div>
                  </TableCell>
                  <TableCell className="font-medium text-foreground">{log.contactName}</TableCell>
                  <TableCell className="font-mono text-sm text-muted-foreground">{log.phoneNumber}</TableCell>
                  <TableCell className="font-mono text-sm">{formatDuration(log.duration)}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">{formatDate(log.timestamp)}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
        
        {filteredLogs.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No call logs found matching your filters.
          </div>
        )}
      </div>
    </div>
  );
}
