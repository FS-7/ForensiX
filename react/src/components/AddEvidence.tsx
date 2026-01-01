import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { CrimeCase } from "@/types/case";

const BACKEND = import.meta.env.VITE_BACKEND;

interface CaseCardProps {
    case_: CrimeCase;
}

export const AddEvidence = ({ case_ }: CaseCardProps) => {
    const { toast } = useToast();

    const [formData, setFormData] = useState({
        case_id: "",
        title: "",
        file: ""
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.title) {
            toast({
                title: "Select Zip file",
            });
            return;
        }

        const form = new FormData(e.target);
        form.append('caseNumber', case_.caseNumber);
        form.append('title', formData.title);

        fetch(BACKEND + 'cases/evidence', {
            method: "POST",
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

    const handleDelete = (id) => {
        const form = new URLSearchParams({
            id: id
        })
        fetch(BACKEND + 'cases/evidence', {
            method: "DELETE",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: form
        })
            .then(
                () => {
                    toast({
                        title: "Evidence Removed Successfully",
                    });
                }
            )
            .catch(
                res => console.log(res)
            )

    }

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