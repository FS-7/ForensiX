import { Navigation } from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Shield, FileText, BarChart3, Search } from "lucide-react";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main>
        <section className="bg-gradient-to-br from-primary to-primary/80 text-primary-foreground py-20">
          <div className="container mx-auto px-4 text-center">
            <Shield className="h-16 w-16 mx-auto mb-6" />
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Crime Case Management System
            </h1>
            <p className="text-lg md:text-xl mb-8 text-primary-foreground/90 max-w-2xl mx-auto">
              Efficient tracking, investigation, and resolution of criminal cases. 
              Streamline your law enforcement operations with our comprehensive system.
            </p>
            <div className="flex gap-4 justify-center">
              <Link to="/cases">
                <Button size="lg" variant="secondary">
                  View All Cases
                </Button>
              </Link>
              <Link to="/new-case">
                <Button size="lg" variant="outline" className="bg-primary-foreground/10 text-primary-foreground border-primary-foreground/20 hover:bg-primary-foreground/20">
                  Report New Case
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <section className="py-16 container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-foreground">
            Key Features
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-6">
              <FileText className="h-12 w-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-foreground">Case Management</h3>
              <p className="text-muted-foreground">
                Organize and track all criminal cases in one centralized system with detailed information and status updates.
              </p>
            </Card>
            
            <Card className="p-6">
              <Search className="h-12 w-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-foreground">Advanced Search</h3>
              <p className="text-muted-foreground">
                Quickly find cases using filters for status, severity, type, and more. Efficient search capabilities at your fingertips.
              </p>
            </Card>
            
            <Card className="p-6">
              <BarChart3 className="h-12 w-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-2 text-foreground">Analytics & Reports</h3>
              <p className="text-muted-foreground">
                Generate comprehensive reports and gain insights into crime trends, case resolution rates, and department performance.
              </p>
            </Card>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Index;
