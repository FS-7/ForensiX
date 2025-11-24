import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { CrimeCase } from "@/types/case";
import { useNavigate } from "react-router-dom";

interface CaseCardProps {
    case_: CrimeCase;
}

const BACKEND = 'http://localhost:5000/'

export const AddEvidence = ({ case_ }: CaseCardProps) => {
    const { toast } = useToast();

    const [formData, setFormData] = useState({
        case_id: "",
        title: "",
        file: ""
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validation
        if (!formData.title) {
            toast({
                title: "Select Zip file",
            });
            return;
        }

        const form = new FormData(e.target);
        form.append('caseNumber', case_.caseNumber);
        form.append('title', formData.title);

        fetch(BACKEND + 'cases/addEvidence', {
            method: "POST",
            headers: {
                //"Content-Type": "application/zip"
            },
            body: form
        })
            .then(
                () => {
                    toast({
                        title: "Evidence Added Successfully",
                    });
                }
            )
            .catch(
                res => console.log(res)
            )

    };
    
    const handleChange = (field: string, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
    };

    return (
        <form id="form" className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
                <Label htmlFor="file">Add Evidence</Label>
                <Input
                    id="title"
                    placeholder="Name"
                    onChange={(e) => handleChange("title", e.target.value)}
                    required
                />
            </div>
            <div className="space-y-2">
                <Label htmlFor="file">Add Evidence File</Label>
                <Input
                    type="file"
                    accept=".zip"
                    id="file"
                    name="file"
                    placeholder="Attach Zip File"
                    onChange={(e) => handleChange("file", e.target.value)}
                    required
                />
            </div>
            <div className="flex gap-4 pt-4">
                <Button type="submit" className="flex-1">
                    Add Evidence
                </Button>
            </div>
        </form>
    )
}