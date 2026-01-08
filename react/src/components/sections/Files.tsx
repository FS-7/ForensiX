import { useState, useMemo } from "react";
import { FilterBar } from "@/components/FilterBar";
import { 
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
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
  //id: string;
  Name: string;
  Type: 'image' | 'video' | 'audio' | 'document' | 'archive' | 'other';
  Size: number;
  Path: string;
  C_TIME: string;
  M_TIME: string;
  Content?: string;
}

export function Files({ report }) {
  const [files, setFiles] = useState(report[0]["Files"])
  
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");

  const formatSize = (size: number) => {
    if (size >= (1024 * 1024 * 1024)) return `${(size * (1024 * 1024 * 1024)).toFixed(0)} GB`;
    if (size >= (1024 * 1024)) return `${(size / (1024 * 1024)).toFixed(2)} MB`;
    if (size >= (1024)) return `${(size / 1024).toFixed(2)} KB`;
    return `${size.toFixed(1)} B`;
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
      
      const matchesType = typeFilter === "all" || file.Type === typeFilter;
      
      return matchesSearch && matchesType;
    });
  }, [search, typeFilter]);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Files</h2>
        <p className="text-muted-foreground">Browse and filter device files</p>
      </div>

      <div className="card-gradient rounded-lg border border-border overflow-hidden animate-fade-in">
        {filteredFiles.length > 0 ? (
          <Accordion type="single" collapsible className="w-full">
            {filteredFiles.map((file) => (
              <AccordionItem key={file.Path} value={file.Name} className="border-border">
                <AccordionTrigger className="px-4 py-3 hover:bg-secondary/50">
                  <div className="flex items-center gap-3 flex-1">
                    <Folder className="w-5 h-5 text-yellow-400" />
                    <div className="flex flex-col items-start">
                      <span className="font-medium text-foreground">{file.Name}</span>
                    </div>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="divide-y divide-border">
                    {files.map((file, i) => {
                      const Icon = fileTypeIcons[file.Type];
                      return (
                        <div
                          key={i}
                          className="px-4 py-3 hover:bg-secondary/30 transition-colors"
                        >
                          {file.Content && (
                              <div className="mt-2 p-3 bg-secondary/50 rounded-md border border-border">
                                <p className="text-xs text-muted-foreground mb-1">Content Preview:</p>
                                <p className="text-foreground whitespace-pre-wrap">{file.Content}</p>
                              </div>
                            )}
                          <div className="flex items-center gap-3 mb-2">
                            <span className="font-medium text-foreground">{file.Path}</span>
                            <Badge variant="outline" className="capitalize text-xs ml-auto">
                              {file.Type}
                            </Badge>
                          </div>
                          <div className="ml-8 text-sm text-muted-foreground space-y-1">
                            <p>Size: <span className="font-mono">{formatSize(file.Size)}</span></p>
                            <p>Created: {formatDate(file.C_TIME)}</p>
                            <p>Modified: {formatDate(file.M_TIME)}</p>
                            
                          </div>
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
            No files found matching your filters.
          </div>
        )}
      </div>

      <div className="text-sm text-muted-foreground text-right">
        Total: {filteredFiles.length} files • {formatSize(filteredFiles.reduce((acc, f) => acc + f.Size, 0))}
      </div>
    </div>
  );
}
