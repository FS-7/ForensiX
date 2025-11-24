import { useParams, Link } from "react-router-dom";
import { Navigation } from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Calendar, MapPin, User, AlertCircle, FileText, Shield } from "lucide-react";
import { CaseNLPChat } from "@/components/CaseNLPChat";
import { useEffect, useState } from "react";
import { Evidence } from "@/components/Evidence";
import CaseReport from "@/components/CaseReport";

const BACKEND = 'http://localhost:5000/'

const CaseDetail = () => {
	const { id } = useParams();
	const [cases, setCases] = useState([])
	useEffect(
		() => {
			async function getCases() {
				await fetch(BACKEND + 'cases',

				)
					.then(
						(res) => {
							if (res.status == 200)
								res.json().then((x) => { setCases(x) })
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
	const case_ = cases.find((c) => c.id === id);

	if (!case_) {
		return (
			<div className="min-h-screen bg-background">
				<Navigation />
				<main className="container mx-auto px-4 py-8 text-center">
					<h1 className="text-2xl font-bold mb-4">Case Not Found</h1>
					<Link to="/cases">
						<Button>Back to Cases</Button>
					</Link>
				</main>
			</div>
		);
	}

	const getStatusColor = (status: string) => {
		switch (status) {
			case "open": return "bg-info text-info-foreground";
			case "investigating": return "bg-warning text-warning-foreground";
			case "pending": return "bg-secondary text-secondary-foreground";
			case "solved": return "bg-success text-success-foreground";
			case "closed": return "bg-muted text-muted-foreground";
			default: return "bg-secondary text-secondary-foreground";
		}
	};

	const getSeverityColor = (severity: string) => {
		switch (severity) {
			case "critical": return "bg-accent text-accent-foreground";
			case "high": return "bg-destructive text-destructive-foreground";
			case "medium": return "bg-warning text-warning-foreground";
			case "low": return "bg-muted text-muted-foreground";
			default: return "bg-muted text-muted-foreground";
		}
	};

	return (
		<div className="min-h-screen bg-background">
			<Navigation />

			<main className="container mx-auto px-4 py-8">
				<div className="mb-6">
					<Link to="/cases">
						<Button variant="ghost" className="gap-2 mb-4">
							<ArrowLeft className="h-4 w-4" />
							Back to Cases
						</Button>
					</Link>

					<div className="flex items-start justify-between">
						<div>
							<h1 className="text-3xl font-bold text-foreground mb-2">{case_.title}</h1>
							<p className="text-muted-foreground">{case_.caseNumber}</p>
						</div>
						<div className="flex gap-2">
							<Badge className={getSeverityColor(case_.severity)}>
								{case_.severity}
							</Badge>
							<Badge className={getStatusColor(case_.status)}>
								{case_.status}
							</Badge>
						</div>
					</div>
				</div>

				<div className="grid lg:grid-cols-3 gap-6">
					{/* Main Content */}
					<div className="lg:col-span-2 space-y-6">
						<CaseNLPChat caseData={case_} />
						<Card className="p-6">
							<h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
								<FileText className="h-5 w-5 text-primary" />
								Case Description
							</h2>
							<p className="text-foreground leading-relaxed">{case_.description}</p>
						</Card>
						<CaseReport case_={case_}/>

						{case_.notes && (
							<Card className="p-6">
								<h2 className="text-xl font-semibold mb-4">Notes</h2>
								<p className="text-muted-foreground">{case_.notes}</p>
							</Card>
						)}
					</div>

					{/* Sidebar */}
					<div className="space-y-6">
						<Evidence case_={case_}/>
						<Card className="p-6">
							<h2 className="text-xl font-semibold mb-4">Case Details</h2>
							<div className="space-y-4">
								<div>
									<div className="flex items-center gap-2 text-muted-foreground mb-1">
										<AlertCircle className="h-4 w-4" />
										<span className="text-sm font-medium">Type</span>
									</div>
									<p className="text-foreground capitalize">{case_.type}</p>
								</div>

								<div>
									<div className="flex items-center gap-2 text-muted-foreground mb-1">
										<MapPin className="h-4 w-4" />
										<span className="text-sm font-medium">Location</span>
									</div>
									<p className="text-foreground">{case_.location}</p>
								</div>

								<div>
									<div className="flex items-center gap-2 text-muted-foreground mb-1">
										<Calendar className="h-4 w-4" />
										<span className="text-sm font-medium">Date Occurred</span>
									</div>
									<p className="text-foreground">
										{new Date(case_.dateOccurred).toLocaleDateString('en-US', {
											year: 'numeric',
											month: 'long',
											day: 'numeric'
										})}
									</p>
								</div>

								<div>
									<div className="flex items-center gap-2 text-muted-foreground mb-1">
										<Calendar className="h-4 w-4" />
										<span className="text-sm font-medium">Date Reported</span>
									</div>
									<p className="text-foreground">
										{new Date(case_.dateReported).toLocaleDateString('en-US', {
											year: 'numeric',
											month: 'long',
											day: 'numeric'
										})}
									</p>
								</div>

								{case_.assignedOfficer && (
									<div>
										<div className="flex items-center gap-2 text-muted-foreground mb-1">
											<User className="h-4 w-4" />
											<span className="text-sm font-medium">Assigned Officer</span>
										</div>
										<p className="text-foreground">{case_.assignedOfficer}</p>
									</div>
								)}

								{case_.witnesses !== undefined && (
									<div>
										<div className="flex items-center gap-2 text-muted-foreground mb-1">
											<User className="h-4 w-4" />
											<span className="text-sm font-medium">Witnesses</span>
										</div>
										<p className="text-foreground">{case_.witnesses}</p>
									</div>
								)}
							</div>
						</Card>
					</div>
				</div>
			</main>
		</div>
	);
};

export default CaseDetail;
