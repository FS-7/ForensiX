import { CrimeCase } from "@/types/case";
import { useEffect, useState } from "react";
import { Card } from "./ui/card";
import { FileText } from "lucide-react";
import { RecentContacts } from "./RecentContacts";
import { ContactCard } from "./ContactCard";

const BACKEND = 'http://localhost:5000/'

interface CaseCardProps {
    case_: CrimeCase;
}

const CaseReport = ({ case_ }: CaseCardProps) => {
    const [report, setReport] = useState([])
    const EvidenceReport = (evidence) => {
        var results = {}
        useEffect(
            () => {
                async function getCases() {
                    console.log("fetching from following\n", BACKEND + 'internal/generateReport/' + evidence)
                    await fetch(BACKEND + 'internal/generateReport/' + evidence,

                    )
                        .then(
                            (res) => {
                                res.json().then(x => setReport(report => report = [...report, x]))
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
    }

    case_.evidences.forEach((evidence) => {
        EvidenceReport(evidence[0])

    })

    return (
        <>
            {
                report.map((i, j) => (

                    <Card className="p-6" key={j}>
                        <h2 className="text-xl font-semibold mb-4">Evidences Summary</h2>
                        <h3 className="text-xl font-semibold mb-4">Messages</h3>
                        {
                            i &&
                            Object.entries(i["text"]).map((i) => (
                                <ContactCard
                                    key={i[0]}
                                    number={i[0]}
                                    label={i[1]}
                                    isThreat={i[1] != "Normal"}
                                />
                            ))
                        }

                        <RecentContacts contacts={i["contacts"]} />
                    </Card>
                ))
            }
        </>
    )
}

export default CaseReport;