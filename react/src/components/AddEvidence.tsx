import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { CrimeCase } from "@/types/case";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";

const BACKEND = import.meta.env.VITE_BACKEND;

interface CaseCardProps {
    case_: CrimeCase;
}

export const AddEvidence = ({ case_ }: CaseCardProps) => {
    const { toast } = useToast();

    const [formData, setFormData] = useState({
        case_id: case_.caseNumber,
        type: "",
        file: ""
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.file) {
            toast({
                title: "Select Zip file",
            });
            return;
        }

        if (!formData.type) {
            toast({
                title: "Select Type",
            });
            return;
        }

        const form = new FormData(e.target);
        form.append('caseNumber', formData.case_id);
        form.append('type', formData.type);

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
                <Select
                    onValueChange={(val) => handleChange("type", val)}
                    required
                >
                    <SelectTrigger>
                        <SelectValue placeholder="Type of Evidence" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="device">Device Data</SelectItem>
                        <SelectItem value="forensic">Forensic Evidence</SelectItem>
                        <SelectItem value="footage">Security Footage</SelectItem>
                    </SelectContent>
                </Select>
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