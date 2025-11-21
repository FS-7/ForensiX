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
import { toast } from "sonner";
import { CrimeCase } from "@/types/case";
import { FileInput } from "lucide-react";

interface CaseCardProps {
    case_: CrimeCase;
}

const BACKEND = 'http://localhost:5000/'

export const AddEvidence = ({ case_ }: CaseCardProps) => {
    const navigate = useNavigate();
    const { toast } = useToast();


    const [evidences, setEvidences] = useState([])
    const [formData, setFormData] = useState({
        case_id: "",
        title: "",
        reference: ""
    });
    
    //let evidences = [{ case_id: "CC-01", title: "Hello", reference: "" }, { case_id: "CC-02", title: "Hi", reference: "" }]

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validation
        if (!formData.title) {
            toast({
                title: "Select Zip file",
            });
            return;
        }
        fetch(BACKEND + 'cases', {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: ""
        })
            .then(
                res => console.log(res)
            )
            .catch(
                res => console.log(res)
            )
        toast({
            title: "Evidence Added Successfully",
        });

        navigate("/cases");
    };
    const handleChange = (field: string, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    return (
        <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Evidences</h2>
            <div className="space-y-4">
                <div>
                    <div className="flex items-center gap-2 text-muted-foreground mb-1">
                        <span className="text-sm font-medium">Evidence</span>
                    </div>
                    {case_.evidence.map((e, i) => (
                        <p className="text-foreground capitalize" key={i}>{e}</p>
                    ))}
                </div>
            </div>
            <form className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="file">Add Evidence</Label>
                    <Input
                        id="title"
                        placeholder="Attach Zip File"
                        value={formData.title}
                        onChange={(e) => handleChange("title", e.target.value)}
                        required
                    />

                </div>
                <div className="flex gap-4 pt-4">
                    <Button type="submit" className="flex-1">
                        Add Evidence
                    </Button>
                </div>
            </form>
        </Card>
    );
};
