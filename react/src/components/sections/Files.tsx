import { useState, useMemo } from "react";
import { deviceFiles } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { 
  Image, 
  Video, 
  Music, 
  FileText, 
  Archive, 
  File,
  Folder
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

const fileTypeIcons = {
  image: Image,
  video: Video,
  audio: Music,
  document: FileText,
  archive: Archive,
  other: File,
};

const fileTypeColors = {
  image: "text-pink-400",
  video: "text-purple-400",
  audio: "text-green-400",
  document: "text-blue-400",
  archive: "text-yellow-400",
  other: "text-gray-400",
};

export interface DeviceFile {
  id: string;
  Name: string;
  type: 'image' | 'video' | 'audio' | 'document' | 'archive' | 'other';
  Size: number;
  Path: string;
  C_TIME: string;
  M_TIME: string;
}

export function Files({report}) {
  const [files, setFiles] = useState(report[0]["Files"] || [])
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");

  const formatSize = (sizeMB: number) => {
    if (sizeMB >= 1024 * 1024 * 1024) return `${(sizeMB / (1024 * 1024 * 1024)).toFixed(0)} GB`;
    if (sizeMB >= 1024 * 1024) return `${(sizeMB / (1024 * 1024)).toFixed(2)} MB`;
    if (sizeMB >= 1024) return `${(sizeMB / 1024).toFixed(2)} KB`;
    return `${sizeMB.toFixed(1)} B`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const filteredFiles = useMemo(() => {
    return files.filter((file) => {
      const matchesSearch = 
        file.Name.toLowerCase().includes(search.toLowerCase()) ||
        file.Path.toLowerCase().includes(search.toLowerCase());
      
      const matchesType = typeFilter === "all" || file.type === typeFilter;
      
      return matchesSearch && matchesType;
    });
  }, [search, typeFilter]);

  const hasActiveFilters = search !== "" || typeFilter !== "all";

  const totalSize = files.reduce((acc, file) => acc + file.size, 0);
  const typeStats = deviceFiles.reduce((acc, file) => {
    acc[file.type] = (acc[file.type] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Files</h2>
        <p className="text-muted-foreground">Browse and filter device files</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
        {Object.entries(fileTypeIcons).map(([type, Icon]) => (
          <button
            key={type}
            onClick={() => setTypeFilter(typeFilter === type ? "all" : type)}
            className={cn(
              "card-gradient rounded-lg border p-3 text-center transition-all",
              typeFilter === type 
                ? "border-primary bg-primary/10" 
                : "border-border hover:border-primary/30"
            )}
          >
            <Icon className={cn("w-5 h-5 mx-auto mb-1", fileTypeColors[type as keyof typeof fileTypeColors])} />
            <p className="text-xs text-muted-foreground capitalize">{type}</p>
            <p className="text-sm font-semibold text-foreground">{typeStats[type] || 0}</p>
          </button>
        ))}
      </div>

      <FilterBar
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search files..."
        hasActiveFilters={hasActiveFilters}
        onClearFilters={() => {
          setSearch("");
          setTypeFilter("all");
        }}
        filters={[
          {
            id: "type",
            label: "File Type",
            value: typeFilter,
            onChange: setTypeFilter,
            options: [
              { value: "all", label: "All Types" },
              { value: "image", label: "Images" },
              { value: "video", label: "Videos" },
              { value: "audio", label: "Audio" },
              { value: "document", label: "Documents" },
              { value: "archive", label: "Archives" },
              { value: "other", label: "Other" },
            ],
          },
        ]}
      />

      <div className="card-gradient rounded-lg border border-border overflow-hidden animate-fade-in">
        <Table>
          <TableHeader>
            <TableRow className="border-border hover:bg-transparent">
              <TableHead className="text-muted-foreground">Name</TableHead>
              <TableHead className="text-muted-foreground">Type</TableHead>
              <TableHead className="text-muted-foreground">Size</TableHead>
              <TableHead className="text-muted-foreground">Path</TableHead>
              <TableHead className="text-muted-foreground">Created</TableHead>
              <TableHead className="text-muted-foreground">Modified</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredFiles.map((file, i) => {
              const Icon = fileTypeIcons[file.type];
              return (
                <TableRow key={i} className="border-border hover:bg-secondary/50">
                  <TableCell>
                    <div className="flex items-center gap-3">
                      <span className="font-medium text-foreground truncate max-w-[200px]">
                        {file.Name}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="capitalize text-xs">
                      {file.type}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-mono text-sm">{formatSize(file.Size)}</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-1 text-sm text-muted-foreground">
                      <Folder className="w-4 h-4" />
                      <span className="truncate max-w-[150px]">{file.Path}</span>
                    </div>
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {formatDate(file.C_TIME)}
                  </TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {formatDate(file.M_TIME)}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
        
        {filteredFiles.length === 0 && (
          <div className="p-8 text-center text-muted-foreground">
            No files found matching your filters.
          </div>
        )}
      </div>

      <div className="text-sm text-muted-foreground text-right">
        Total: {filteredFiles.length} files • {formatSize(totalSize)}
      </div>
    </div>
  );
}
