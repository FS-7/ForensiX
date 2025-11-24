import { CrimeCase } from "@/types/case";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { FileText } from "lucide-react";

const BACKEND = 'http://localhost:5000/'

interface CaseCardProps {
    case_: CrimeCase;
}

const CaseReport = ({ case_ }: CaseCardProps) => {
    const [report, setReport] = useState({})
    const EvidenceReport = (evidence) => {
        var results = {}
        useEffect(
            () => {
                async function getCases() {
                    await fetch(BACKEND + 'internal/generateReport/' + evidence,

                    )
                        .then(
                            (res) => {
                                res.json().then(x => setReport(x))
                            }
                        )
                        .catch(
                            (res) => {
                                console.log(res)
                            }
                        )
                }
                getCases()
            },
            []
        )
        return results
    }

    for (let evidence in case_.evidences) {
        EvidenceReport(case_.evidences[evidence][0])
        console.log(report["text"])
    }

    return (
        <>
            {
                <Card className="p-6">
                    <h2 className="text-xl font-semibold mb-4">Evidences</h2>
                    {
                        report["text"] && report["text"].length > 0 &&
                        Object.entries(report["text"]).map( ([k, v], i) => (
                            <div className="space-y-4" key={i}>
                                <div>
                                    <div className="flex items-center gap-2 text-muted-foreground mb-1">
                                        <span className="text-sm font-medium">Evidence: </span>
                                        <p className="text-foreground capitalize">{k}: {report["text"][v]}</p>
                                    </div>
                                </div>
                            </div>
                        ))
                    }
                </Card>
            }
        </>
    )
}

export default CaseReport;