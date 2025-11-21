import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Navigation } from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";

const BACKEND = 'http://localhost:5000/'

const NewCase = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    type: "",
    severity: "",
    location: "",
    dateOccurred: "",
    assignedOfficer: "",
    witnesses: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.title || !formData.description || !formData.type || !formData.severity) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      });
      return;
    }
    fetch(BACKEND + 'cases', {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        title: formData['title'],
        description: formData['description'],
        type: formData['type'],
        severity: formData['severity'],
        location: formData['location'],
        dateOccurred: formData['dateOccurred'],
        assignedOfficer: formData['assignedOfficer'],
        witnesses: formData['witnesses'],
      })
    })
    .then(
      res => console.log(res)
    )
    .catch(
      res => console.log(res)
    )
    toast({
      title: "Case Reported Successfully",
      description: "The case has been added to the system.",
    });
    
    navigate("/cases");
  };

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Report New Case</h1>
            <p className="text-muted-foreground">
              Fill in the details to create a new crime case report
            </p>
          </div>

          <Card className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="title">Case Title *</Label>
                <Input
                  id="title"
                  placeholder="Brief description of the incident"
                  value={formData.title}
                  onChange={(e) => handleChange("title", e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  placeholder="Detailed description of the incident"
                  value={formData.description}
                  onChange={(e) => handleChange("description", e.target.value)}
                  rows={5}
                  required
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="type">Case Type *</Label>
                  <Select value={formData.type} onValueChange={(value) => handleChange("type", value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="theft">Theft</SelectItem>
                      <SelectItem value="assault">Assault</SelectItem>
                      <SelectItem value="fraud">Fraud</SelectItem>
                      <SelectItem value="vandalism">Vandalism</SelectItem>
                      <SelectItem value="homicide">Homicide</SelectItem>
                      <SelectItem value="cybercrime">Cybercrime</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="severity">Severity *</Label>
                  <Select value={formData.severity} onValueChange={(value) => handleChange("severity", value)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select severity" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                      <SelectItem value="critical">Critical</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  placeholder="Street address or area"
                  value={formData.location}
                  onChange={(e) => handleChange("location", e.target.value)}
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="dateOccurred">Date Occurred</Label>
                  <Input
                    id="dateOccurred"
                    type="date"
                    value={formData.dateOccurred}
                    onChange={(e) => handleChange("dateOccurred", e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="witnesses">Number of Witnesses</Label>
                  <Input
                    id="witnesses"
                    type="number"
                    min="0"
                    placeholder="0"
                    value={formData.witnesses}
                    onChange={(e) => handleChange("witnesses", e.target.value)}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="assignedOfficer">Assigned Officer</Label>
                <Input
                  id="assignedOfficer"
                  placeholder="Officer name"
                  value={formData.assignedOfficer}
                  onChange={(e) => handleChange("assignedOfficer", e.target.value)}
                />
              </div>

              <div className="flex gap-4 pt-4">
                <Button type="submit" className="flex-1">
                  Submit Case Report
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate("/cases")}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default NewCase;
