import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const BACKEND = 'http://localhost:5000/'

const CaseReport = () => {
    const { id } = useParams();
    const [report, setReport] = useState([])
    useEffect(
        () => {
            async function getCases() {
                await fetch(BACKEND + 'threat/analyze',

                )
                    .then(
                        (res) => {
                            if (res.status == 200)
                                res.json().then((x) => { setReport(x) })
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
    console.log(report)

    return(<></>)
}

export default CaseReport;