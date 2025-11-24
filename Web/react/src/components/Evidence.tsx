import { CrimeCase } from "@/types/case";
import { Card } from "./ui/card";
import { AddEvidence } from "./AddEvidence";

interface CaseCardProps {
    case_: CrimeCase;
}

export const Evidence = ({ case_ }: CaseCardProps) => {
    return (
        <Card className="p-6">
            <AddEvidence case_={case_} />
            <br/>
            <hr/>
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
        </Card>
    );
};
