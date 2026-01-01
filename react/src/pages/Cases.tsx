import { useEffect, useState } from "react";
import { Navigation } from "@/components/Navigation";
import { CaseCard } from "@/components/CaseCard";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Search } from "lucide-react";

const BACKEND = import.meta.env.VITE_BACKEND;

const Cases = () => {
	const [cases, setCases] = useState([])
	useEffect(
		() => {
			async function getCases() {
				await fetch(BACKEND + '/cases',

				)
				.then(
					(res) => {
						if(res.status == 200)
							res.json().then((x) => {setCases(x)})
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
	
	const [searchTerm, setSearchTerm] = useState("");
	const [statusFilter, setStatusFilter] = useState("all");
	const [severityFilter, setSeverityFilter] = useState("all");

	const filteredCases = cases.filter((case_) => {
		const matchesSearch =
			case_.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
			case_.caseNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
			case_.description.toLowerCase().includes(searchTerm.toLowerCase());

		const matchesStatus = statusFilter === "all" || case_.status === statusFilter;
		const matchesSeverity = severityFilter === "all" || case_.severity === severityFilter;

		return matchesSearch && matchesStatus && matchesSeverity;
	});

	return (
		<div className="min-h-screen bg-background">
			<Navigation />

			<main className="container mx-auto px-4 py-8">
				<div className="mb-8">
					<h1 className="text-3xl font-bold text-foreground mb-2">Case Management</h1>
					<p className="text-muted-foreground">
						View and manage all crime cases in the system
					</p>
				</div>

				{/* Filters */}
				<div className="mb-6 grid md:grid-cols-4 gap-4">
					<div className="md:col-span-2 relative">
						<Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
						<Input
							placeholder="Search cases..."
							value={searchTerm}
							onChange={(e) => setSearchTerm(e.target.value)}
							className="pl-9"
						/>
					</div>

					<Select value={statusFilter} onValueChange={setStatusFilter}>
						<SelectTrigger>
							<SelectValue placeholder="Filter by status" />
						</SelectTrigger>
						<SelectContent>
							<SelectItem value="all">All Statuses</SelectItem>
							<SelectItem value="open">Open</SelectItem>
							<SelectItem value="investigating">Investigating</SelectItem>
							<SelectItem value="pending">Pending</SelectItem>
							<SelectItem value="solved">Solved</SelectItem>
							<SelectItem value="closed">Closed</SelectItem>
						</SelectContent>
					</Select>

					<Select value={severityFilter} onValueChange={setSeverityFilter}>
						<SelectTrigger>
							<SelectValue placeholder="Filter by severity" />
						</SelectTrigger>
						<SelectContent>
							<SelectItem value="all">All Severities</SelectItem>
							<SelectItem value="critical">Critical</SelectItem>
							<SelectItem value="high">High</SelectItem>
							<SelectItem value="medium">Medium</SelectItem>
							<SelectItem value="low">Low</SelectItem>
						</SelectContent>
					</Select>
				</div>

				{/* Results Count */}
				<div className="mb-4 text-sm text-muted-foreground">
					Showing {filteredCases.length} of {cases.length} cases
				</div>

				{/* Cases Grid */}
				<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
					{filteredCases.map((case_) => (
						<CaseCard key={case_.id} case_={case_} />
					))}
				</div>

				{filteredCases.length === 0 && (
					<div className="text-center py-12">
						<p className="text-muted-foreground">No cases found matching your filters.</p>
					</div>
				)}
			</main>
		</div>
	);
};

export default Cases;
