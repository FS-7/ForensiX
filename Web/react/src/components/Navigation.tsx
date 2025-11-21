import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Shield, FileText, PlusCircle } from "lucide-react";

export const Navigation = () => {
  const location = useLocation();
  
  const isActive = (path: string) => location.pathname === path;
  
  return (
    <nav className="border-b border-border bg-card shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 text-primary font-bold text-xl">
            <Shield className="h-6 w-6" />
            <span>CrimeTrack</span>
          </Link>
          
          <div className="flex items-center gap-2">
            <Link to="/cases">
              <Button 
                variant={isActive("/cases") ? "default" : "ghost"}
                className="gap-2"
              >
                <FileText className="h-4 w-4" />
                Cases
              </Button>
            </Link>
            <Link to="/new-case">
              <Button 
                variant={isActive("/new-case") ? "default" : "ghost"}
                className="gap-2"
              >
                <PlusCircle className="h-4 w-4" />
                New Case
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};
